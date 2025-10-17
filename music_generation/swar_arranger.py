
import random
from config import SWAR_FREQUENCIES, OCTAVE_MULTIPLIERS

# ----------------------------------------
# Helper: Scale Definitions
# ----------------------------------------
SCALE_ORDER = ["Sa", "Re", "Ga", "Ma", "Pa", "Dh", "Ni"]

# ----------------------------------------
# Helper Functions
# ----------------------------------------
def get_index(note):
    return SCALE_ORDER.index(note) if note in SCALE_ORDER else -1

def get_note(idx):
    return SCALE_ORDER[idx] if 0 <= idx < len(SCALE_ORDER) else None

# ----------------------------------------
# 1. ORIGINAL SWAR ARRANGEMENT
# ----------------------------------------
def arrange_swar_sequence(swar_source, total_duration=10.0, music_params=None):
    tempo_multiplier = music_params.get("tempo_multiplier", 1.0) if music_params else 1.0
    volume_min, volume_max = music_params.get("volume_range", (0.6,1.0)) if music_params else (0.6,1.0)
    notes_per_phrase = random.randint(6,9)  # variable phrase length

    avg_note_duration = 0.4 / tempo_multiplier
    total_notes = int(total_duration / avg_note_duration)

    # Normalize source
    swar_freq_list = []
    if isinstance(swar_source[0][1], str):
        for swar, octv in swar_source:
            base = SWAR_FREQUENCIES.get(swar, 0.0)
            multi = OCTAVE_MULTIPLIERS.get(octv, 1.0)
            swar_freq_list.append((swar, base * multi))
    else:
        swar_freq_list = swar_source.copy()

    idx_map = {s: i for i, s in enumerate(SCALE_ORDER)}

    # 1) Logical Phrase Generation with up to 2 repeats max
    sequence = []
    prev1 = prev2 = None
    # start on Sa if possible
    current = next(((s,f) for s,f in swar_freq_list if s=="Sa"), swar_freq_list[0])
    sequence.append(current)
    prev1 = current[0]

    for _ in range(total_notes - 1):
        # occasional rest
        if random.random() < 0.1 and prev1 != "Rest":
            sequence.append(("Rest", 0.0))
            prev2, prev1 = prev1, "Rest"
            continue

        last_idx = idx_map.get(prev1, 0)
        direction = random.choice([-1, 1])
        step = 1 if random.random() < 0.7 else 2
        next_idx = max(0, min(last_idx + direction*step, len(SCALE_ORDER)-1))

        candidates = [it for it in swar_freq_list
                      if idx_map.get(it[0], -1) == next_idx]

        # fallback to near-range
        if not candidates:
            candidates = [it for it in swar_freq_list
                          if abs(idx_map.get(it[0],0) - last_idx) <= 2]

        # enforce max 2 repeats
        filtered = [c for c in candidates
                    if not (c[0] == prev1 == prev2)]
        pick_list = filtered or candidates or swar_freq_list
        nxt = random.choice(pick_list)

        sequence.append(nxt)
        prev2, prev1 = prev1, nxt[0]

    # 2) Jitter smoothing
    jitters = [random.uniform(-0.25,0.25) for _ in sequence]
    smooth_jitters = []
    for i in range(len(jitters)):
        win = jitters[max(0,i-1):min(len(jitters),i+2)]
        smooth_jitters.append(sum(win)/len(win))

    # 3) Finalize note events
    final = []
    for idx, ((swar,freq), j) in enumerate(zip(sequence, smooth_jitters), 1):
        if swar == "Rest":
            dur = avg_note_duration * random.uniform(0.4,0.6)
            final.append({'swar':'Re','frequency':0.0,'duration':dur,'volume':0.0})
            continue
        dur = max(0.2, avg_note_duration*(1+j))
        if idx % notes_per_phrase == 0:
            dur *= 1.2
        vol = random.uniform(volume_min, volume_max)
        final.append({'swar':swar,'frequency':freq,'duration':dur,'volume':vol})

    # 4) Soft Asc/Desc Phrases with small swaps, no >2 repeats
    for i in range(0, len(final), notes_per_phrase):
        block = final[i:i+notes_per_phrase]
        notes = [n for n in block if n['volume']>0]
        if not notes: continue

        sorted_notes = sorted(notes, key=lambda x: x['frequency'])
        order = sorted_notes.copy()
        for j in range(len(order)-1):
            if random.random() < 0.3:
                order[j],order[j+1] = order[j+1],order[j]
        seq_ord = order if random.random()<0.5 else list(reversed(order))
        it = iter(seq_ord)
        for j in range(len(block)):
            if block[j]['volume']>0:
                candidate = next(it)
                # enforce ≤2 repeats
                prev_vals = [block[k]['swar'] for k in range(max(0,j-2), j)]
                if prev_vals.count(candidate['swar']) < 2:
                    block[j] = candidate
        final[i:i+notes_per_phrase] = block

    return final

# ----------------------------------------
# 2. ENHANCED SWAR SEQUENCE BUILDER
# ----------------------------------------
# 50 handcrafted melodic phrases
PHRASES = [
    ['Sa','Re','Ga','Ma'], ['Pa','Dh','Ni','Sa'], ['Ga','Re','Sa','Ni'],
    ['Ma','Ga','Re','Sa'], ['Sa','Re','Ma','Pa'], ['Ga','Ma','Pa','Dh'],
    ['Dha','Ni','Sa','Re'], ['Pa','Ma','Ga','Re'], ['Ni','Re','Ma','Pa'],
    ['Ga','Pa','Dh','Ni'], ['Sa','Ga','Ni','Pa'], ['Pa','Ga','Ma','Re'],
    ['Ni','Dha','Pa','Ma'], ['Sa','Re','Ga','Ma','Pa'], ['Pa','Ma','Ga','Re','Sa'],
    ['Ma','Pa','Dh','Ni','Sa'], ['Re','Ga','Ma','Pa','Dha'], ['Ga','Ma','Pa','Ni','Sa'],
    ['Ma','Dh','Pa','Re','Sa'], ['Pa','Ni','Sa','Re','Ga'], ['Sa','Pa','Ma','Ga'],
    ['Re','Sa','Ni','Dha'], ['Ga','Re','Sa','Pa'], ['Ma','Ga','Re','Ni'],
    ['Pa','Sa','Re','Ga'], ['Dha','Pa','Ma','Re'], ['Ni','Ma','Ga','Re'],
    ['Sa','Re','Pa','Sa'], ['Re','Ga','Pa','Ni'], ['Ga','Ma','Ni','Sa'],
    ['Ma','Pa','Sa','Re'], ['Pa','Dha','Re','Sa'], ['Dha','Ni','Ga','Ma'],
    ['Ni','Sa','Pa','Ma'], ['Sa','Ma','Pa','Ga'], ['Re','Pa','Dha','Ni'],
    ['Ga','Sa','Re','Ni'], ['Ma','Sa','Ga','Dha'], ['Pa','Re','Sa','Ni'],
    ['Dha','Ga','Ma','Pa'], ['Ni','Pa','Re','Sa'], ['Sa','Re','Ga'],
    ['Re','Ga','Ma'], ['Ga','Ma','Pa'], ['Ma','Pa','Dha'], ['Pa','Dha','Ni'],
    ['Dha','Ni','Sa'], ['Ni','Sa','Re'], ['Sa','Re','Ga','Ma','Pa','Dha','Ni']
]

# Markov transitions
TRANSITIONS = {
    'Sa': ['Re', 'Ga', 'Ma', 'Pa'],
    'Re': ['Sa', 'Ga', 'Ma', 'Pa', 'Dha'],
    'Ga': ['Re', 'Ma', 'Pa', 'Dha', 'Ni'],
    'Ma': ['Ga', 'Pa', 'Dha', 'Ni', 'Sa'],
    'Pa': ['Ma', 'Dha', 'Ni', 'Sa', 'Re'],
    'Dha': ['Pa', 'Ni', 'Sa', 'Re', 'Ga'],
    'Ni': ['Dha', 'Sa', 'Re', 'Ga', 'Ma']
}

def generate_markov_sequence(length, swar_pool):
    seq = [random.choice(swar_pool)]

    def is_valid(candidate):
        temp = seq + [candidate]
        for k in [2, 3]:
            if len(temp) >= k * 2:
                a, b = temp[-k:], temp[-2 * k:-k]
                c = temp[-3 * k:-2 * k] if len(temp) >= 3 * k else []
                if a == b == c:
                    return False
        return True

    while len(seq) < length:
        curr = seq[-1]
        opts = TRANSITIONS.get(curr, swar_pool)
        valid = [n for n in opts if n in swar_pool and is_valid(n)]
        seq.append(random.choice(valid if valid else swar_pool))
    return seq

def insert_phrases(base_seq, swar_pool, every=8):
    out = []
    phrases = PHRASES.copy()
    random.shuffle(phrases)
    for i in range(0, len(base_seq), every):
        chunk = base_seq[i:i+every]
        # avoid >2 at boundary
        for n in chunk:
            if len(out)>=2 and out[-1]==out[-2]==n: continue
            out.append(n)
        if random.random()<0.6:
            p = random.choice(phrases)
            for x in p:
                if x in swar_pool and not(len(out)>=2 and out[-1]==out[-2]==x):
                    out.append(x)
    return out[:len(base_seq)]

def smooth_melody(seq, swar_pool):
    out = []
    for a,b in zip(seq, seq[1:]):
        out.append(a)
        i1,i2 = get_index(a), get_index(b)
        if abs(i1 - i2) > 2:
            step = 1 if i2>i1 else -1
            for j in range(i1+step, i2, step):
                note = get_note(j)
                if note in swar_pool and not(len(out)>=2 and out[-1]==out[-2]==note):
                    out.append(note)
    out.append(seq[-1])
    return out

def enhance_swar_sequence(swar_source, total_duration=10.0, music_params=None):
    tempo = music_params.get("tempo_multiplier",1.0) if music_params else 1.0
    avg = 0.4/tempo
    count = int(total_duration/avg)

    # build pool & freq
    if isinstance(swar_source[0][1], str):
        pool = [s for s,_ in swar_source]
        freq_map = {s: SWAR_FREQUENCIES.get(s,0.0)*OCTAVE_MULTIPLIERS.get(o,1.0)
                    for s,o in swar_source}
    else:
        pool = [s for s,_ in swar_source]
        freq_map = {s:f for s,f in swar_source}

    raw = generate_markov_sequence(count, pool)
    phrased = insert_phrases(raw, pool, every=random.randint(6,9))
    smooth = smooth_melody(phrased, pool)

    sequence = []
    for s in smooth[:count]:
        sequence.append({
            'swar': s,
            'frequency': freq_map.get(s,0.0),
            'duration': random.choice([0.5,0.75,1.0]),
            'volume': 1.0
        })
    return sequence

<script>
  import CaesarViz from './lib/components/CaesarViz.svelte'
  import VigenereViz from './lib/components/VigenereViz.svelte'
  import TranspositionViz from './lib/components/TranspositionViz.svelte'
  import PlayfairViz from './lib/components/PlayfairViz.svelte'
  import SubstitutionViz from './lib/components/SubstitutionViz.svelte'
  import { fetchCiphers, runCipher } from './lib/api.js'

  const ICONS = {
    caesar: '🏛️', vigenere: '🔐', transposition: '🧩', playfair: '⬛', substitution: '🔤'
  }
  const ORDER = ['caesar', 'vigenere', 'transposition', 'playfair', 'substitution']

  let ciphers = $state({})
  let active = $state('caesar')
  let text = $state('KRIPTOGRAFI KLASIK')
  let key = $state('3')
  let mode = $state('encrypt')
  let loading = $state(false)
  let error = $state('')
  let result = $state(null)
  let step = $state(-1)
  let playing = $state(false)
  let timer = null

  const meta = $derived(ciphers[active] ?? {})
  const totalSteps = $derived(
    result ? (active === 'transposition' ? (result.col_order?.length ?? 0) : (result.steps?.length ?? 0)) : 0
  )

  async function load() {
    try { ciphers = await fetchCiphers(); selectCipher('caesar') } catch (e) { error = e.message }
  }

  function selectCipher(name) {
    active = name
    const m = ciphers[name]
    key = m?.key_default ?? ''
    result = null; error = ''; stopPlay(); step = -1
  }

  function switchMode(m) {
    mode = m; result = null; stopPlay(); step = -1
  }

  async function run() {
    if (!text.trim()) { error = 'Teks tidak boleh kosong.'; return }
    loading = true; error = ''; stopPlay(); step = -1
    try {
      result = await runCipher(active, { text, key, mode })
    } catch (e) {
      error = e.message; result = null
    } finally {
      loading = false
    }
  }

  function stopPlay() { playing = false; if (timer) { clearInterval(timer); timer = null } }
  function play() {
    if (!totalSteps) return
    if (step < 0 || step >= totalSteps - 1) step = 0
    playing = true
    timer = setInterval(() => {
      if (step >= totalSteps - 1) { stopPlay(); return }
      step += 1
    }, 650)
  }
  function next() { stopPlay(); step = Math.min((step < 0 ? -1 : step) + 1, totalSteps - 1) }
  function prev() { stopPlay(); step = Math.max((step < 0 ? totalSteps : step) - 1, 0) }
  function showAll() { stopPlay(); step = -1 }

  load()
</script>

<main class="min-h-screen">
  <!-- HEADER -->
  <header class="border-b border-slate-800/80 backdrop-blur bg-slate-950/60 sticky top-0 z-20">
    <div class="max-w-7xl mx-auto px-5 py-4 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl grid place-items-center bg-gradient-to-br from-cyan-400 to-violet-500 text-slate-950 font-black">C</div>
        <div>
          <h1 class="font-bold text-lg leading-none">Crypto Lab</h1>
          <p class="text-xs text-slate-400">Visualisasi 5 algoritma cipher klasik</p>
        </div>
      </div>
      <div class="flex gap-2 text-xs">
        <span class="px-3 py-1.5 rounded-lg border border-slate-800 text-slate-400">Svelte 5</span>
        <span class="px-3 py-1.5 rounded-lg border border-slate-800 text-slate-400">Python · Flask</span>
      </div>
    </div>
  </header>

  <div class="max-w-7xl mx-auto px-5 py-6 grid lg:grid-cols-[260px_1fr] gap-6">
    <!-- SIDEBAR -->
    <aside class="space-y-2">
      <div class="text-xs uppercase tracking-widest text-slate-500 px-2 mb-1">Algoritma</div>
      {#each ORDER as name}
        {@const m = ciphers[name]}
        <button onclick={() => selectCipher(name)}
          class="w-full text-left px-3 py-3 rounded-xl border transition flex items-center gap-3
          {active === name
            ? 'border-cyan-400/60 bg-cyan-500/10 shadow-[0_0_20px_-6px_rgba(34,211,238,.5)]'
            : 'border-slate-800 hover:border-slate-700 hover:bg-slate-900/60'}">
          <span class="text-xl">{ICONS[name]}</span>
          <span class="min-w-0">
            <span class="block font-semibold text-sm truncate">{m?.label ?? name}</span>
            <span class="block text-[11px] text-slate-400 truncate">{m?.family ?? ''}</span>
          </span>
        </button>
      {/each}

      <div class="mt-4 p-3 rounded-xl border border-slate-800 bg-slate-900/40 text-[11px] leading-relaxed text-slate-400">
        <b class="text-slate-300">Substitusi</b> mengganti <i>identitas</i> huruf.
        <b class="text-slate-300">Transposisi</b> mengubah <i>urutan</i> huruf.
      </div>
    </aside>

    <!-- KONTEN -->
    <section class="space-y-6 min-w-0">
      <!-- info cipher -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 slideup" key={active}>
        <div class="flex items-start gap-3">
          <span class="text-2xl">{ICONS[active]}</span>
          <div>
            <h2 class="text-xl font-bold">{meta.label}</h2>
            <p class="text-xs text-cyan-400/80 uppercase tracking-widest">{meta.family}</p>
            <p class="text-sm text-slate-300 mt-2">{meta.desc}</p>
          </div>
        </div>
      </div>

      <!-- form -->
      <div class="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 space-y-4">
        <div class="grid md:grid-cols-[1fr_220px] gap-4">
          <label class="block">
            <span class="text-xs uppercase tracking-widest text-slate-400">Teks masukan</span>
            <textarea bind:value={text} rows="3"
              class="mt-1.5 w-full rounded-xl bg-slate-950/70 border border-slate-800 focus:border-cyan-400/60 focus:outline-none p-3 font-mono text-sm resize-y"
              placeholder="Tulis teks di sini..."></textarea>
          </label>
          <label class="block">
            <span class="text-xs uppercase tracking-widest text-slate-400">{meta.key_label}</span>
            {#if meta.key_type === 'number'}
              <input type="number" min="0" max="25" bind:value={key}
                class="mt-1.5 w-full rounded-xl bg-slate-950/70 border border-slate-800 focus:border-cyan-400/60 focus:outline-none p-3 font-mono text-sm" />
              <span class="text-[11px] text-slate-500">0–25</span>
            {:else}
              <input type="text" bind:value={key}
                class="mt-1.5 w-full rounded-xl bg-slate-950/70 border border-slate-800 focus:border-cyan-400/60 focus:outline-none p-3 font-mono text-sm uppercase tracking-widest" />
              <span class="text-[11px] text-slate-500">huruf saja</span>
            {/if}
          </label>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <div class="inline-flex rounded-xl border border-slate-800 overflow-hidden">
            <button onclick={() => switchMode('encrypt')}
              class="px-4 py-2 text-sm font-medium {mode === 'encrypt' ? 'bg-cyan-500/20 text-cyan-200' : 'text-slate-400 hover:bg-slate-800/60'}">🔒 Enkripsi</button>
            <button onclick={() => switchMode('decrypt')}
              class="px-4 py-2 text-sm font-medium border-l border-slate-800 {mode === 'decrypt' ? 'bg-violet-500/20 text-violet-200' : 'text-slate-400 hover:bg-slate-800/60'}">🔓 Dekripsi</button>
          </div>
          <button onclick={run} disabled={loading}
            class="px-6 py-2.5 rounded-xl font-semibold text-slate-950 bg-gradient-to-r from-cyan-400 to-cyan-300 hover:from-cyan-300 hover:to-cyan-200 disabled:opacity-50 transition">
            {loading ? 'Memproses…' : 'Jalankan ⚡'}
          </button>
        </div>

        {#if error}
          <div class="text-sm text-rose-300 bg-rose-500/10 border border-rose-500/30 rounded-xl px-4 py-3">
            ⚠ {error}
          </div>
        {/if}
      </div>

      <!-- HASIL -->
      {#if result}
        <div class="rounded-2xl border border-cyan-500/30 bg-gradient-to-b from-cyan-500/5 to-transparent p-5 slideup">
          <div class="text-xs uppercase tracking-widest text-cyan-400/80 mb-2">Hasil</div>
          <div class="font-mono text-xl break-all text-amber-200 selection:bg-amber-400/30">{result.result}</div>
          <div class="mt-2 text-xs text-slate-500 font-mono">
            masukan bersih: {result.input_clean} ({result.input_clean.length} huruf)
          </div>
        </div>

        <!-- KONTROL LANGKAH -->
        {#if totalSteps > 0}
          <div class="rounded-2xl border border-slate-800 bg-slate-900/40 p-4">
            <div class="flex flex-wrap items-center gap-3">
              <span class="text-xs uppercase tracking-widest text-slate-400">Visualisasi langkah</span>
              <div class="flex items-center gap-2 ml-auto">
                <button onclick={prev} class="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-sm">◀</button>
                {#if playing}
                  <button onclick={stopPlay} class="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-sm">⏸</button>
                {:else}
                  <button onclick={play} class="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-sm">▶ Play</button>
                {/if}
                <button onclick={next} class="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-sm">▶</button>
                <button onclick={showAll} class="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-sm">Semua</button>
              </div>
            </div>
            <input type="range" min="0" max={Math.max(totalSteps - 1, 0)} value={step < 0 ? totalSteps - 1 : step}
              oninput={(e) => { stopPlay(); step = +e.currentTarget.value }}
              class="w-full mt-3 accent-cyan-400" />
            <div class="text-[11px] text-slate-500 font-mono">
              langkah {(step < 0 ? totalSteps : step + 1)} / {totalSteps}
            </div>
          </div>

          <!-- VISUALISASI per tipe -->
          <div class="rounded-2xl border border-slate-800 bg-slate-900/40 p-5">
            {#if active === 'caesar'}
              <CaesarViz data={result} {step} />
            {:else if active === 'vigenere'}
              <VigenereViz data={result} {step} />
            {:else if active === 'transposition'}
              <TranspositionViz data={result} {step} />
            {:else if active === 'playfair'}
              <PlayfairViz data={result} {step} />
            {:else if active === 'substitution'}
              <SubstitutionViz data={result} {step} />
            {/if}
          </div>
        {/if}
      {/if}

      <footer class="text-center text-xs text-slate-600 pt-4 pb-8">
        Crypto Lab · Caesar · Vigenère · Columnar Transposition · Playfair · Keyword Substitution — logika di Python, tampilan di Svelte 5.
      </footer>
    </section>
  </div>
</main>

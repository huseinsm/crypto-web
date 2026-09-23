<script>
  import CaesarViz from './lib/components/CaesarViz.svelte'
  import VigenereViz from './lib/components/VigenereViz.svelte'
  import TranspositionViz from './lib/components/TranspositionViz.svelte'
  import PlayfairViz from './lib/components/PlayfairViz.svelte'
  import SubstitutionViz from './lib/components/SubstitutionViz.svelte'
  import { fetchCiphers, runCipher } from './lib/api.js'

  const MONO = {
    caesar: 'C', vigenere: 'V', transposition: 'T', playfair: 'P', substitution: 'S'
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
  <header class="sticky top-0 z-20 border-b border-line bg-paper/90 backdrop-blur">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 grid place-items-center rounded-md bg-ink text-paper font-serif font-semibold text-lg">C</div>
        <div>
          <h1 class="font-serif font-semibold text-lg leading-tight">Crypto Lab</h1>
          <p class="text-[13px] text-ink-3">Visualisasi algoritma cipher klasik</p>
        </div>
      </div>
      <div class="text-[13px] text-ink-3 font-mono">Svelte 5 · Python · Flask</div>
    </div>
  </header>

  <div class="max-w-6xl mx-auto px-6 py-8 grid lg:grid-cols-[240px_1fr] gap-8">
    <!-- SIDEBAR -->
    <aside>
      <div class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold mb-3 px-1">Algoritma</div>
      <nav class="space-y-1">
        {#each ORDER as name}
          {@const m = ciphers[name]}
          <button onclick={() => selectCipher(name)}
            class="w-full text-left px-3 py-2.5 rounded-lg border transition flex items-center gap-3
            {active === name
              ? 'bg-surface border-line-strong shadow-sm'
              : 'border-transparent hover:bg-surface/70'}">
            <span class="w-7 h-7 grid place-items-center rounded-md border font-serif font-semibold text-[13px] shrink-0
              {active === name ? 'bg-brand text-white border-brand' : 'bg-paper text-ink-2 border-line'}">{MONO[name]}</span>
            <span class="min-w-0">
              <span class="block text-sm font-medium truncate {active === name ? 'text-ink' : 'text-ink-2'}">{m?.label ?? name}</span>
              <span class="block text-[11px] text-ink-3 truncate">{m?.family ?? ''}</span>
            </span>
          </button>
        {/each}
      </nav>

      <div class="mt-6 p-3.5 rounded-lg border border-line bg-surface text-[12px] leading-relaxed text-ink-2">
        <b class="text-ink">Substitusi</b> mengganti identitas huruf,
        <b class="text-ink">transposisi</b> mengubah urutannya.
      </div>
    </aside>

    <!-- KONTEN -->
    <section class="space-y-5 min-w-0">
      <!-- info cipher -->
      <div class="rounded-xl border border-line bg-surface p-5 fadeup" key={active}>
        <div class="flex items-baseline gap-3 flex-wrap">
          <h2 class="font-serif text-2xl font-semibold text-ink">{meta.label}</h2>
          <span class="text-[11px] uppercase tracking-[0.14em] text-brand font-semibold">{meta.family}</span>
        </div>
        <p class="text-sm text-ink-2 mt-2 leading-relaxed">{meta.desc}</p>
      </div>

      <!-- form -->
      <div class="rounded-xl border border-line bg-surface p-5 space-y-4">
        <div class="grid md:grid-cols-[1fr_200px] gap-4">
          <label class="block">
            <span class="text-xs font-semibold uppercase tracking-[0.12em] text-ink-3">Teks masukan</span>
            <textarea bind:value={text} rows="3"
              class="mt-2 w-full rounded-lg bg-paper border border-line focus:border-brand focus:ring-2 focus:ring-brand/15 focus:outline-none p-3 font-mono text-sm resize-y text-ink"
              placeholder="Tulis teks di sini..."></textarea>
          </label>
          <label class="block">
            <span class="text-xs font-semibold uppercase tracking-[0.12em] text-ink-3">{meta.key_label}</span>
            {#if meta.key_type === 'number'}
              <input type="number" min="0" max="25" bind:value={key}
                class="mt-2 w-full rounded-lg bg-paper border border-line focus:border-brand focus:ring-2 focus:ring-brand/15 focus:outline-none p-3 font-mono text-sm text-ink" />
              <span class="text-[11px] text-ink-3 mt-1 block">0–25</span>
            {:else}
              <input type="text" bind:value={key}
                class="mt-2 w-full rounded-lg bg-paper border border-line focus:border-brand focus:ring-2 focus:ring-brand/15 focus:outline-none p-3 font-mono text-sm uppercase tracking-widest text-ink" />
              <span class="text-[11px] text-ink-3 mt-1 block">huruf saja</span>
            {/if}
          </label>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <div class="inline-flex rounded-lg border border-line overflow-hidden bg-paper">
            <button onclick={() => switchMode('encrypt')}
              class="px-4 py-2 text-sm font-medium transition
              {mode === 'encrypt' ? 'bg-ink text-paper' : 'text-ink-2 hover:text-ink'}">Enkripsi</button>
            <button onclick={() => switchMode('decrypt')}
              class="px-4 py-2 text-sm font-medium transition border-l border-line
              {mode === 'decrypt' ? 'bg-ink text-paper' : 'text-ink-2 hover:text-ink'}">Dekripsi</button>
          </div>
          <button onclick={run} disabled={loading}
            class="px-6 py-2.5 rounded-lg font-semibold text-sm text-white bg-brand hover:bg-brand-deep disabled:opacity-50 transition">
            {loading ? 'Memproses…' : 'Jalankan'}
          </button>
        </div>

        {#if error}
          <div class="text-sm text-danger bg-danger-soft border border-danger/25 rounded-lg px-4 py-3">
            {error}
          </div>
        {/if}
      </div>

      <!-- HASIL -->
      {#if result}
        <div class="rounded-xl border border-line bg-surface p-5 fadeup">
          <div class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold mb-3">Hasil</div>
          <div class="font-mono text-xl break-all text-ink leading-snug">{result.result}</div>
          <div class="mt-2 text-xs text-ink-3 font-mono">
            masukan bersih: {result.input_clean} ({result.input_clean.length} huruf)
          </div>
        </div>

        <!-- KONTROL LANGKAH -->
        {#if totalSteps > 0}
          <div class="rounded-xl border border-line bg-surface p-4">
            <div class="flex flex-wrap items-center gap-3">
              <span class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold">Langkah</span>
              <div class="flex items-center gap-1.5 ml-auto">
                <button onclick={prev} aria-label="Sebelumnya" class="p-2 rounded-md border border-line text-ink-2 hover:bg-paper hover:text-ink transition">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
                </button>
                {#if playing}
                  <button onclick={stopPlay} aria-label="Jeda" class="p-2 rounded-md border border-line text-ink-2 hover:bg-paper hover:text-ink transition">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>
                  </button>
                {:else}
                  <button onclick={play} class="px-3 py-2 rounded-md border border-line text-[13px] font-medium text-ink-2 hover:bg-paper hover:text-ink transition">Putar</button>
                {/if}
                <button onclick={next} aria-label="Berikutnya" class="p-2 rounded-md border border-line text-ink-2 hover:bg-paper hover:text-ink transition">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg>
                </button>
                <button onclick={showAll} class="px-3 py-2 rounded-md border border-line text-[13px] font-medium text-ink-2 hover:bg-paper hover:text-ink transition">Semua</button>
              </div>
            </div>
            <input type="range" min="0" max={Math.max(totalSteps - 1, 0)} value={step < 0 ? totalSteps - 1 : step}
              oninput={(e) => { stopPlay(); step = +e.currentTarget.value }}
              class="w-full mt-3 accent-brand" />
            <div class="text-[11px] text-ink-3 font-mono mt-1">
              langkah {(step < 0 ? totalSteps : step + 1)} / {totalSteps}
            </div>
          </div>

          <!-- VISUALISASI per tipe -->
          <div class="rounded-xl border border-line bg-surface p-5">
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

      <footer class="text-center text-xs text-ink-3 pt-2 pb-6">
        Caesar · Vigenère · Columnar Transposition · Playfair · Keyword Substitution — logika di Python, antarmuka di Svelte 5.
      </footer>
    </section>
  </div>
</main>

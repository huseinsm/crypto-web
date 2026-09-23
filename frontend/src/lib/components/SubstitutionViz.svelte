<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
  const cur = $derived(active >= 0 ? steps[active] : null)

  const plain = $derived(data.plain_alphabet.split(''))
  const cipher = $derived(data.cipher_alphabet.split(''))
  const hiPlain = $derived(cur ? cur.char : null)
</script>

<div class="space-y-5">
  <div class="text-xs uppercase tracking-[0.14em] text-brand font-semibold">
    {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'} · kata kunci: {data.key.key}
  </div>

  <!-- tabel substitusi 26 kolom -->
  <div class="overflow-x-auto">
    <div class="inline-block">
      <div class="text-[10px] uppercase tracking-[0.14em] text-brand mb-1">Alfabet asli</div>
      <div class="flex gap-1 mb-2">
        {#each plain as ch, i}
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {ch === hiPlain ? 'bg-brand text-white border-brand' : 'bg-paper border-line text-ink-2'}">
            {ch}
          </div>
        {/each}
      </div>
      <div class="text-center text-ink-3 text-xs mb-1">↓ substitusi ↓</div>
      <div class="text-[10px] uppercase tracking-[0.14em] text-gold mb-1">Alfabet cipher</div>
      <div class="flex gap-1">
        {#each cipher as ch, i}
          <div class="w-8 h-8 grid place-items-center rounded font-mono text-sm border
            {cur && cur.cipher === ch ? 'bg-gold-soft border-gold/50 text-gold' : 'bg-paper border-line text-gold/70'}">
            {ch}
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- peta A->Z dll -->
  <details>
    <summary class="cursor-pointer text-xs uppercase tracking-[0.14em] text-ink-3 hover:text-brand font-semibold select-none">
      Tabel pemetaan lengkap
    </summary>
    <div class="mt-3 grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-1.5 font-mono text-xs">
      {#each plain as ch, i}
        <div class="px-2 py-1 rounded border border-line bg-paper">
          <span class="text-brand">{ch}</span>
          <span class="text-ink-3 mx-1">→</span>
          <span class="text-gold">{cipher[i]}</span>
        </div>
      {/each}
    </div>
  </details>

  <!-- langkah huruf -->
  {#if cur}
    <div class="text-sm text-ink-2 font-mono border-l-2 border-brand/40 pl-3">
      huruf ke-{cur.i}: <span class="text-brand">{cur.char}</span>
      → <span class="text-gold font-semibold">{cur.cipher}</span>
    </div>
  {/if}
  <div class="text-sm font-mono text-ink-2">
    Hasil: <span class="text-gold">{data.result}</span>
  </div>
</div>

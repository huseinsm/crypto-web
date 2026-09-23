<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-[0.14em] text-brand font-semibold">
    Geseran {data.key.shift} · {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'}
  </div>

  <div class="flex flex-wrap gap-2">
    {#each steps as s, i}
      <div class="flex flex-col items-center gap-1">
        <div class="w-9 h-9 grid place-items-center rounded-md font-mono text-sm border
          {i <= active ? 'bg-brand-soft border-brand/40 text-brand-deep' : 'bg-paper border-line text-ink-3'}">
          {s.char}
        </div>
        <div class="text-[10px] text-ink-3 font-mono">{s.index}→{s.new_index}</div>
        <div class="w-9 h-9 grid place-items-center rounded-md font-mono text-sm border
          {i <= active ? 'bg-gold-soft border-gold/40 text-gold' : 'bg-paper border-line text-ink-3'}">
          {i <= active ? s.cipher : '?'}
        </div>
      </div>
    {/each}
  </div>

  <div class="flex flex-wrap items-center gap-2 text-xs text-ink-2 font-mono">
    <span class="px-2 py-1 rounded border border-line bg-paper">A=0 … Z=25</span>
    <span class="px-2 py-1 rounded border border-line bg-paper">rumus: (P + {data.key.shift}) mod 26</span>
  </div>

  {#if data.brute_force && data.brute_force.length}
    <div class="pt-2">
      <div class="text-xs uppercase tracking-[0.14em] text-ink-3 font-semibold mb-2">Brute force — coba semua geseran</div>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
        {#each data.brute_force as b}
          <div class="font-mono text-xs px-2 py-1.5 rounded border border-line bg-paper">
            <span class="text-ink-3">k={b.shift}</span>
            <span class="text-ink ml-2">{b.hasil}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

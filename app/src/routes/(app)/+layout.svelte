<script lang="ts">
	import NavBar from './NavBar.svelte'
	let { children } = $props();
</script>

<div class="card border-surface-100-900 grid h-[640px] w-full grid-cols-[auto_1fr] border-[1px] h-screen">
	<div>
		<NavBar />
	</div>
  <div class="flex items-center justify-center">
		{@render children()}
  </div>
</div>

<script lang="ts">
  import { Navigation } from '@skeletonlabs/skeleton-svelte';
  // Icons
  import IconMenu from '@lucide/svelte/icons/menu';
  import IconFolder from '@lucide/svelte/icons/folder';
  import IconSettings from '@lucide/svelte/icons/settings';
	import { ChartColumn } from '@lucide/svelte';
</script>

<Navigation.Rail>
  {#snippet tiles()}
    <Navigation.Tile label="Projects" href="/projects"><IconFolder /></Navigation.Tile>
    <Navigation.Tile label="Stats" href="/stats"><ChartColumn/></Navigation.Tile>
  {/snippet}
  {#snippet footer()}
    <Navigation.Tile labelExpanded="Settings" href="#settings" title="settings"><IconSettings /></Navigation.Tile>
  {/snippet}
</Navigation.Rail>

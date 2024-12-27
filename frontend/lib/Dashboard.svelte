<script lang="ts">
    import { onMount } from "svelte";
    import { link } from "@dvcol/svelte-simple-router/router";
    import { getBackendUrl } from "$lib/utils.js";
    let printers: string[] = [];

    let url = getBackendUrl();

    onMount(async () => {
        try {
            const response = await fetch(url + "/api/printers");
            if (!response.ok) throw new Error("Failed to fetch printers");
            printers = await response.json();
        } catch (error) {
            console.error("Error fetching printers:", error);
        }
    });
</script>

<h1>Available Printers</h1>
<div class="printer-list">
    {#if printers.length > 0}
        <ul>
            {#each printers as printer}
                <li>
                    <a href="/printer?printerId={printer}" use:link>{printer}</a>
                </li>
            {/each}
        </ul>
    {:else}
        <p>Loading printers...</p>
    {/if}
</div>

<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { useRoute } from "@dvcol/svelte-simple-router/router";

    const { route, location, routing } = useRoute();
    const queryParams = $derived(location.query);

    let imageUrl = $state<string | null>(null);
    let ws = $state<WebSocket | null>(null);
    let connectionError = $state<string | null>(null);

    function getBackendUrl(): string {
        let url = import.meta.env.VITE_BACKEND_URL;

        if (url) {
            url = "http://" + url;
        } else {
            url = "";
        }

        return url;
    }

    function connect() {
        const backendUrl = getBackendUrl();
        ws = new WebSocket(`${backendUrl}/ws/printer/${queryParams["printerId"]}`);

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === "jpeg_image") {
                const binaryData = atob(message.data);
                const bytes = new Uint8Array(binaryData.length);
                for (let i = 0; i < binaryData.length; i++) {
                    bytes[i] = binaryData.charCodeAt(i);
                }
                const blob = new Blob([bytes], { type: "image/jpeg" });

                if (imageUrl) {
                    URL.revokeObjectURL(imageUrl);
                }
                imageUrl = URL.createObjectURL(blob);
            }
        };

        ws.onerror = (error) => {
            connectionError = "Connection error occurred";
            console.error("WebSocket error:", error);
        };

        ws.onclose = (event) => {
            if (event.code === 4004) {
                connectionError = "Invalid printer name";
            }
        };
    }

    onMount(() => {
        connect();
    });

    onDestroy(() => {
        if (ws) {
            ws.close();
        }
        if (imageUrl) {
            URL.revokeObjectURL(imageUrl);
        }
    });
</script>

<div class="printer-camera">
    {#if connectionError}
        <div class="error">{connectionError}</div>
    {:else if imageUrl}
        <img src={imageUrl} alt="Printer camera feed" />
    {:else}
        <div class="loading">Connecting to printer camera...</div>
    {/if}
</div>

<style>
    .printer-camera {
        width: 100%;
        max-width: 640px;
        aspect-ratio: 16/9;
        background: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .error {
        color: red;
    }

    .loading {
        color: #666;
    }
</style>

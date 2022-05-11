<script>
    import { onMount } from "svelte";

    let statusCode = 200;

    onMount(async () => {
        let resp = await fetch("http://127.0.0.1:8000/api/auth/signup/").then((res) => res.json());
        console.log(resp);
        statusCode = resp.statusCode;
        console.log(statusCode);
        });
</script>

<main>
    <h1>Hello!</h1>
    <p>
        Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn
        how to build Svelte apps.
    </p>

    <h3>Data from server</h3>
</main>
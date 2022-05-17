<script>
    import { Router, Route } from "svelte-navigator";
    import { onMount } from 'svelte';

    import isAuthenticated from "./healpers/IsAuthenticated"

    import Home from "./routes/Home.svelte";
    import Register from "./routes/Register.svelte";
    import NotFound from "./routes/NotFound.svelte";
    import Login from "./routes/Login.svelte";

    onMount(() => {
        isAuthenticated();
    });

</script>
<svelte:head>
    <title>THis Is Test</title>
    <!-- Font Awesome -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    rel="stylesheet"
    />
    <!-- Google Fonts -->
    <link
    href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
    rel="stylesheet"
    />
    <!-- MDB -->
    <link
    href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.css"
    rel="stylesheet"
    />
    <script
        type="text/javascript"
        src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.js"
        defer
    ></script>
    <style>
        body {
            padding: 0 8px !important;
        }
    </style>
</svelte:head>

<main>
    <Router>
        <Route path="/" component={Home} />
        <Route path="auth/login/" component={Login} />
        <Route path="auth/register/" component={Register} />
        <Route component={NotFound} />
        <Route component={NotFound} />
    </Router>
</main>

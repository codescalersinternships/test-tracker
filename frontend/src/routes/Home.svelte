<script>
    import { Router, Link } from "svelte-navigator";
</script>

<svelte:head>
  <title>Welcome</title>
</svelte:head>
<Router>
    <Link to="/">Home</Link>
    <Link to="auth/register/">Register</Link>
</Router>
<h1>Hello and welcome to my site!</h1>
<script>
    import { onMount } from "svelte";

    import axios from "../healpers/axios";
    import NavBar from "../components/NavBar.svelte";
    import Input from "../components/ui/Input.svelte";
    import LoodingSpiner from "../components/ui/LoodingSpiner.svelte";
    import { updateSettingsFields } from "../healpers/fields"
    import { validateFields } from "../healpers/validateFields"
    import Alert from "../components/ui/Alert.svelte";

    export let user;
    let mode, sun, moon, showAlert, _class, message;

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };

    function logger(_class_, _message_) {
        showAlert = true;
        _class = _class_;
        message = _message_;
    };

    onMount(async () => {
        mode = localStorage.getItem("mode");
        if(mode === "light"){
            sun = true;
            moon = false;
        } else if(mode === "dark"){
            moon = true;
            sun = false;
        }
    });

    async function updateSettings(){
        let body = updateSettingsFields(user);
        if (user.password1 !== undefined || user.password2 !== undefined){
            if (user.password1 !== user.password2) {
                logger("danger", "password mismatch.");
                return;
            } else {
                body.password = user.password1;
            }
        }
        if (!validateFields(body)){
            logger("danger", "Please fill all fields.");
            return;
        }

        if (body.phone.toString().length > 15 || body.phone.toString().length < 9){
            logger("danger", "Invalid phone number.");
            return;
        }

        const response = await axios.put("auth/settings/", body, config);

        if(response.status === 201){
            logger("success", response.data.message);
            setTimeout(() => {
                showAlert = false;
            }, 1500);
        } else {
            logger("danger", response.data.message);
        }
    };

    function changeMode() {
        mode = localStorage.getItem("mode")
        console.log(mode);
        if(mode === "light"){
            window.document.body.classList.remove('light');
            window.document.body.classList.add('dark');
            localStorage.setItem("mode", "dark");
            sun = false;
            moon = true;
        } else if(mode === "dark"){
            window.document.body.classList.remove('dark');
            window.document.body.classList.add('light');
            localStorage.setItem("mode", "light");
            moon = false;
            sun = true;
        }
    }
</script>

<section>
    {#if user}
        <NavBar projectView="true" 
            {user}
        />
        <div class="container pt-4">
            <div class="mb-4">
                <div class="row">
                    <div class="col-11" style="overflow: hidden;">
                        <strong class="h4">Settings | 
                            <strong class="text-primary">{user.first_name} {user.last_name}</strong>
                        </strong>
                    </div>
                    <div class="col-1">
                        {#if sun}
                            <button class="change-mode sun-btn" on:click={changeMode}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-moon-stars moon" viewBox="0 0 16 16">
                                    <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278zM4.858 1.311A7.269 7.269 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.316 7.316 0 0 0 5.205-2.162c-.337.042-.68.063-1.029.063-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286z"/>
                                    <path d="M10.794 3.148a.217.217 0 0 1 .412 0l.387 1.162c.173.518.579.924 1.097 1.097l1.162.387a.217.217 0 0 1 0 .412l-1.162.387a1.734 1.734 0 0 0-1.097 1.097l-.387 1.162a.217.217 0 0 1-.412 0l-.387-1.162A1.734 1.734 0 0 0 9.31 6.593l-1.162-.387a.217.217 0 0 1 0-.412l1.162-.387a1.734 1.734 0 0 0 1.097-1.097l.387-1.162zM13.863.099a.145.145 0 0 1 .274 0l.258.774c.115.346.386.617.732.732l.774.258a.145.145 0 0 1 0 .274l-.774.258a1.156 1.156 0 0 0-.732.732l-.258.774a.145.145 0 0 1-.274 0l-.258-.774a1.156 1.156 0 0 0-.732-.732l-.774-.258a.145.145 0 0 1 0-.274l.774-.258c.346-.115.617-.386.732-.732L13.863.1z"/>
                                </svg>
                            </button>
                        {:else if moon}
                            <button class="change-mode moon-btn" on:click={changeMode}>
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-brightness-high sun" viewBox="0 0 16 16">
                                    <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0zm0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13zm8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5zM3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8zm10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0zm-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0zm9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707zM4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708z"/>
                                </svg>
                            </button>
                        {/if}
                    </div>
                </div>
            </div>
            <section class="section-tabs">
                <ul class="nav nav-tabs mb-5" id="ex1" role="tablist">
                    <li class="nav-item nav-style" role="presentation">
                        <a
                            class="nav-link nav-link-tab active"
                            id="ex1-tab-1"
                            data-mdb-toggle="tab"
                            href="#ex1-tabs-1"
                            role="tab"
                            aria-controls="ex1-tabs-1"
                            aria-selected="true">profile information</a
                        >
                    </li>
                    <li class="nav-item nav-style" role="presentation">
                        <a
                            class="nav-link nav-link-tab"
                            id="ex1-tab-2"
                            data-mdb-toggle="tab"
                            href="#ex1-tabs-2"
                            role="tab"
                            aria-controls="ex1-tabs-2"
                            aria-selected="false">security</a
                        >
                    </li>
                </ul>

                <!-- Tabs content -->
                <div class="tab-content" id="ex1-content">
                    <div
                        class="tab-pane fade show active"
                        id="ex1-tabs-1"
                        role="tabpanel"
                        aria-labelledby="ex1-tab-1">
                        <div class="card card-style">
                            <small class="text-center pt-2 pb-0 mb-0">
                                <span class="text-danger">
                                    * Hint - 
                                </span>
                                you are not allowed to change your email.
                            </small>
                            <Input
                                title={"Email."} 
                                type={"email"} 
                                disabled={true} 
                                bind:value={user.email}
                                id={"email"}
                            />
                            <Input
                                title={"First Name."}
                                type={"text"}
                                bind:value={user.first_name}
                                id={"fname"}
                            />
                            <Input
                                title={"Last Name."} 
                                type={"text"} 
                                bind:value={user.last_name}
                                id={"lname"}
                            />
                            <Input
                                title={"Phone Number."} 
                                type={"number"} 
                                bind:value={user.phone}
                                id={"phone"}
                            />
                        </div>
                    </div>
                    <div
                        class="tab-pane fade"
                        id="ex1-tabs-2"
                        role="tabpanel"
                        aria-labelledby="ex1-tab-2"
                        >
                        <div class="card card-style">
                            {#if user.permission !== "admin"}
                                <small class="text-center pt-2 pb-0 mb-0">
                                    <span class="text-danger">
                                        * Hint - 
                                    </span>
                                    Only the host who can set your permission.
                                </small>
                                <Input
                                    title={"Permission."} 
                                    type={"text"}
                                    bind:value={user.permission}
                                    disabled={true}
                                    id={"permission"}
                                />
                            {/if}
                            <Input
                                title={"Password."} 
                                type={"password"} 
                                id={"password"}
                                bind:value={user.password1}
                            />
                            <Input
                                title={"RE Password."} 
                                type={"password"}
                                id={"re-password"} 
                                bind:value={user.password2}
                            />
                        </div>
                    </div>
                    {#if showAlert}
                        <Alert {showAlert} {_class} {message} />
                    {/if}
                    <div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                        <button type="button" class="btn btn-primary btn-lg" 
                            on:click={updateSettings}>
                            Save
                        </button>
                    </div>
                </div>
            </section>
        </div>
    {:else}
        <LoodingSpiner />
    {/if}
</section>
<svelte:head>
    <title>Test-Tracker | Settings</title>
    <style>
        .nav-style {
            width: 50%;
            text-align: center;
        }
        .card-style {
            border: 1px solid #dadada;
            margin-bottom: 15px;
        }
        .change-mode{
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
        }
        .sun{
            color: #ff9900;
        }
        .moon{
            color: #222;
        }
    </style>
</svelte:head>
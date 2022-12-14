
<script>
    import axios from '../healpers/axios'
    import { getToken, getUser } from '../healpers/github_login'
    import GithubLogin from "svelte-github-login";
    import Alert from "../components/ui/Alert.svelte";
    import Input from "../components/ui/Input.svelte";
    import Loadingbtn from "../components/ui/Loadingbtn.svelte"

    let _alert = false, loadingServerBTN, loadingGithub, formDisabled;
    let email, password, message, _class;

    function showAlert(_class_, _message_) {
        _class = _class_;
        message = _message_;
        _alert = true;
    };

    async function github(code){
        loadingGithub = true;
        formDisabled = true;
        const accessToken = await getToken(code);
        const user = await getUser(accessToken);
        const token = user.data.data.access_token;
        localStorage.setItem("token", token);
        window.location.href = '/';
        loadingGithub = false;
        formDisabled = false;
    };


    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
        };

    async function loginApi(){
        loadingServerBTN = true;
        formDisabled = true;
        const data = { email, password};
        if (!email || !password) {
            showAlert('danger', 'Please fill all fields');
            return;
        };
        try {
            if (!validateEmail(email)) {
                showAlert('danger', 'Please enter valid email');
                return;
            };
            const response = await axios.post('/auth/login/', data);
            const token = response.data.access_token;
            localStorage.setItem("token", token);
            if (!localStorage.getItem("mode")){
                localStorage.setItem("mode", "light");
            }
            window.location.href = '/';
        } catch (err) {
            if (err.response.status === 404) {
                showAlert('danger', err.response.data.detail);
            } else if (err.response.status === 401) {
                showAlert('danger', err.response.data.detail);
            } else if (err.response.status === 400) {
                showAlert('danger', err.response.data.detail);
            } else {
                showAlert('danger', 'Something went wrong');
            };  
        } finally {
            loadingServerBTN = false;
            formDisabled = false;
        }
    }

</script>

<svelte:head>
    <title>Test-Tracker | Login</title>
</svelte:head>


<section class="vh-100">
    <div class="container py-5 h-100">
        <div class="row d-flex align-items-center justify-content-center h-100">
            <div class="col-md-8 col-lg-7 col-xl-6">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg"
                class="img-fluid" alt="Phoneimage">
            </div>
            <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
                <form>
                    <div class="pb-4">
                        <p class="h5">
                            We were missing you!
                        </p>
                    </div>
                    <Input 
                        bind:value={email} 
                        id={"email"} 
                        title={"Email"} 
                        type={"email"}
                    />
                    <Input 
                        bind:value={password} 
                        id={"password"} 
                        title={"Password"} 
                        type={"password"}
                    />
                    <Alert showAlert={_alert} message={message} _class={_class} />
                    <div class="d-flex justify-content-center mx-4 pt-2 mb-lg-4">
                        <button type="button" class="w-100 btn btn-primary btn-lg" 
                            on:click={loginApi} disabled={formDisabled}>
                            {#if loadingServerBTN}
                                <Loadingbtn />
                            {:else}
                                Login
                            {/if}
                        </button>
                    </div>
                </form>
                <div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                    <GithubLogin
                        clientId="cbe847a6d887c0ed34a2"
                        scope="user:email,read:org"
                        redirectUri="http://localhost:8080/auth/login"
                        on:success={params => github(params.detail.code)}
                        on:error={error => console.log(error)}
                        let:onLogin
                        >
                        <button class="btn btn-primary w-100 btn-lg"
                            on:click={onLogin}
                            disabled={formDisabled}
                        >
                            {#if loadingGithub}
                                <Loadingbtn />
                            {:else}
                                Login via GitHub
                            {/if}
                        </button>
                    </GithubLogin>
                </div>
            </div>
        </div>
    </div>
</section>

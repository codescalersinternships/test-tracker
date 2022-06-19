
<script>
    import axios from '../healpers/axios'
    import Alert from "../components/ui/Alert.svelte";

    let _alert = false;
    let email, password, message, _class;

    function showAlert(_class_, _message_) {
        _class = _class_;
        message = _message_;
        _alert = true;
    };

    const validateEmail = (email) => {
        return String(email)
            .toLowerCase()
            .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            );
        };

    async function loginApi(){
        const data = { email, password};
        if (! email || ! password) {
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
        };
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
                    <div class="form-outline mb-4">
                        <input bind:value={email} type="email" id="email" class="form-control form-control-lg" />
                        <label class="form-label" for="email">Email</label>
                    </div>
                    <div class="form-outline mb-4">
                        <input bind:value={password} type="password" id="password" class="form-control form-control-lg" />
                        <label class="form-label" for="password">Password</label>
                    </div>
                    <Alert showAlert={_alert} message={message} _class={_class} />
                    <div class="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                        <button type="button" class="btn btn-primary btn-lg" 
                            on:click={loginApi}>
                            Login
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>

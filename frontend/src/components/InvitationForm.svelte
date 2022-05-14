<script>
    import axios from '../healpers/axios'
    import Button from "./Button.svelte";
    export let data;

    async function RegisterApi(){
        const password1 = document.getElementById('password1').value;
        const password2 = document.getElementById('password2').value;
        if (password1 != password2) {
            alert("Passwords do not match");
            return;
        }
        data.password = password1
        try {
            const response = await axios.post("auth/signup/", data)
        if (response.status === 201) { await InviteSuccess() }} 
        catch(err) {
            console.log(err.response.data.error);
        }
    }
    async function InviteSuccess() {
        const urlParams = new URLSearchParams(window.location.search);
        let signature = urlParams.get('signature');
        try {
            const success = await axios.put(`auth/invitation/?signature=${signature}`, data)
        if (success.status === 200) { window.location.href = '/' }} 
        catch(err) {
            console.log(err.response.data.error);
        }
    }
</script>

<main>
    <section class="vh-100">
        <div class="container py-5 h-100">
        <div class="row d-flex align-items-center justify-content-center h-100">
            <div class="col-md-8 col-lg-7 col-xl-6">
            <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg"
                class="img-fluid" alt="Phoneimage">
            </div>
            <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
                <form>
                    <div class="mb-3">
                        <span class="h5">Email:</span> <span class="text-muted grey-text h5"> {data.email}</span>
                    </div>
                    <!-- Password input -->
                    <div class="form-outline mb-4">
                        <input type="password" id="password1" class="form-control form-control-lg" />
                        <label class="form-label" for="password1">Password</label>
                    </div>
                    <!-- Re Password input -->
                    <div class="form-outline mb-4">
                        <input type="password" id="password2" class="form-control form-control-lg" />
                        <label class="form-label" for="password2">Re Password</label>
                    </div>
                    <!-- Submit button -->
                    <Button Class="primary" Function={RegisterApi} text="Register" />
                </form>
            </div>
        </div>
        </div>
    </section>
</main>
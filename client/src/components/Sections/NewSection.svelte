<script>
    import Input from '../ui/Input.svelte';
    import { newSectionFields } from "../../healpers/fields"
    import { validateFields } from "../../healpers/validateFields"
    import Loadingbtn from '../ui/Loadingbtn.svelte';
    import axios from "../../healpers/axios";
    import Alert from '../ui/Alert.svelte';

    export let value;
    

    let form = newSectionFields()
    let isLoading = false;
    let showAlert = false;
    let alertMessage, alertClassName;

    async function postNewSection(){
        isLoading = true;
        const config = {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        };

        if (!validateFields(form.fields)){
            alertMessage = "Please fill all fields";
            alertClassName = "danger";
        };
        
        try {
            const response = await axios.post(
                form.url, form.fields, config
            );
            alertMessage = response.data.message;
            alertClassName = "success";
            form.fields.title = "";
        } catch (error) {
            if (error.response.status != 200){
                alertMessage = error.message;
                alertClassName = "danger";
            };
        } finally {
            showAlert = true;
            isLoading = false;
            setTimeout(
                () => {
                    if(alertClassName == "success"){
                        showAlert = false;
                        value = false;
                    }
                }, 5000
            );
        };
    };

</script>

<div class="col-12">
    <div class="card test_case_card">
        <div class="test_case_info">
            <div class="row" style="margin-left: 10px;">
                <div class="col-7">
                    <Input 
                        bind:value={form.fields.title} 
                        id={"new-section"} 
                        title={"New Section"} 
                        type={"text"}
                    />
                </div>
                <div class="col-3 mt-4 d-flex align-items-center justify-content-end">
                    <button
                        disabled={form.fields.title.length == 0}
                        class="btn new-section-button-api" 
                        on:click={postNewSection}>
                        {#if isLoading}
                            <Loadingbtn />
                        {:else}
                            Add new section
                        {/if}
                    </button>
                </div>
                <div class="col-2 mt-4 d-flex align-items-center justify-content-start">
                    <button
                        class="btn btn-outline-danger default-text-color" 
                        on:click={() => {
                            value = false; // To show the add new section button again.
                        }}>
                        Cancel
                    </button>
                </div>
            </div>
            <Alert showAlert={showAlert} message={alertMessage} _class={alertClassName}/>
        </div>
    </div>
</div>
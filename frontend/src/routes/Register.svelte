<script>
    import { onMount } from 'svelte';
    import axios from '../healpers/axios'
    import Register from 'components/RegisterForms.svelte';
    import InvitationForm from 'components/InvitationForm.svelte';

    const urlParams = new URLSearchParams(window.location.search);
    const signatureParam = urlParams.has('signature');
    let signature = urlParams.get('signature');
    let data = {}

    if (signatureParam){
        onMount(async () => {
            try {
                const response = await axios.get(`auth/invitation/?signature=${signature}`, data)
            if (response.status === 200) { data = response.data.data }} 
            catch(err) {
                window.location.href = '/not-found'
            }
        });
    }

</script>

{#if signatureParam}
    <InvitationForm data={data}/>
{:else}
    <Register />
{/if}
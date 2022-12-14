<script>
    export let value = false;
    export let label;
    export let onClick
    let checkBox;
    let checkSpan;
</script>


<div class="mt-2 mb-2 p-relative">
    <div class="row">
        <div class="col-2">
            <div class:checkbox--checked="{value === true}" class="check-box" bind:this={checkBox} on:click|preventDefault={() => {
                value = checkBox.classList.toggle("checkbox--checked");
                checkSpan.classList.toggle("checkbox-span-checked");
                onClick();
            }}>
                <span class:checkbox-span-checked="{value === true}" class="checkbox-span" bind:this={checkSpan}></span>
            </div>
        </div>
        <div class="col-10 align-items-center d-flex">
            <div class="label">{label}</div>
        </div>
    </div>
</div>



<style>
    .p-relative{
        position: relative;
    }
</style>
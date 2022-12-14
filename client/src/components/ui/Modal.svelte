<script>
    export let show;
</script>

<div class="modal" style={`display: ${show ? "block" : "none"};`}>
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <slot name="modal-header"></slot>
            </div>
            <div class="modal-body">
                <slot name="modal-body"></slot>
            </div>
            <div class="modal-footer">
                <slot name="modal-footer"></slot>
            </div>
        </div>
    </div>
</div>
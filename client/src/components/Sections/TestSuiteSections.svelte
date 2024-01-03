<script>
    import { onMount } from "svelte";
    import axios from "../../healpers/axios";
    import LoadingComponent from "../ui/LoodingSpiner.svelte"
    import DraggableSections from "./DraggableSections.svelte"
    export let projectID;
    export let testSuite;
    export let postedSection;

    let isLoading = false;
    let sections;

    onMount(async () => {
        isLoading = true;
        const config = {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        };
        const response = await axios.get(
            `/test_suites/${projectID}/section/${testSuite.id}/`, config
        );
        sections = response.data.results
        isLoading = false;
    });

    const updateSections = () => {
        if(postedSection){
            sections = sections;
            sections.unshift(postedSection);
            console.log(postedSection);
        }
        // postedSection = undefined;
    };

    $: postedSection, updateSections();

</script>

{#if isLoading}
    <LoadingComponent />
{:else if sections}
    <DraggableSections testSuite={testSuite} list={sections} />
{/if}


<svelte:head>
    <title>Test-Tracker | Test Suite Detail</title>
    <style>
        .title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #5a79b1;
        }
        ul {
            margin: 0;
        }
        h1 {
            font-size: 1.5rem;
        }
        h3 {
            font-size: 20px;
        }
        .card_info {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding: 20px;
            margin-bottom: 20px;
        }
        .card_info p {
            font-size: 20px;
            font-weight: 700;
        }

        .test_case_card {
            position: relative;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 0px;
        }
        .test_case_card a {
            text-decoration: none;
            color: #5a79b1;
            display: block;
            font-weight: 700;
        }
        .collapse_span {
            position: absolute;
            right: 10px;
            height: 30px;
            width: 30px;
            text-align: center;
            border-radius: 50%;
            top: 15px;
        }
        .test_case_info {
            margin-top: 10px;
            padding: 5px;
        }
        .collapse-style {
            margin-left: 25px;
            margin-top: 15px;
        }
        .collapse-style a {
            display: inline;
            color: rgb(90 121 177);
            font-size: 20px;
            cursor: pointer;
        }
        .dropdown-toggle:after {
            display: none;
            margin-left: 0.255em;
            vertical-align: 0.255em;
            content: "";
            border-top: 0.3em solid;
            border-right: 0.3em solid rgb(0 0 0 / 0%);
            border-bottom: 0;
            border-left: 0.3em solid rgb(0 0 0 / 0%);
        }
        .dropdowncustom{
            position: absolute;
            font-size: 0;
            right: 0;
            top:20px
        }
    </style>
</svelte:head>

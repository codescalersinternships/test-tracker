<script>
    import calendarize from '../healpers/calendarize';
    import { onMount } from "svelte";
    import axios from '../healpers/axios';
    import LoodingSpiner from "./ui/LoodingSpiner.svelte"
	
    export let today = null; // Date
    let path = window.location.pathname;
    let testRunID = path.split("/")[4];
	let offset = 0;

	let month = today.getMonth();
	let year = today.getFullYear();
    let loading,testlodge, report = [];

    const config = {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    };
	
	export let labels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
	export let months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
	
	$: today_month = today && today.getMonth();
	$: today_year = today && today.getFullYear();
	$: today_day = today && today.getDate();
	
	let prev = calendarize(new Date(year, month-1), offset);
	let current = calendarize(new Date(year, month), offset);
	let next = calendarize(new Date(year, month+1), offset);
	
	function isToday(day) {
		return today && today_year === year && today_month === month && today_day === day;
	}

    onMount(async () => {
        loading = true;
        const response = await axios.get(`test_runs/month/report/cases/?run=${testRunID}&month=${month+1}`, config)
        report = response.data.data;
        loading = false;
    });
</script>

{#if loading}
    <LoodingSpiner />
{:else}
    <div class="card test_case_card">
        <p class="h5 text-primary">
            Total test cases running based on 
            {months[today_month]}
        </p>
        <div class="card test_case_info c-p-20">
            <div class="month">
                {#each labels as txt, idx (txt)}
                    <span class="label">{ labels[(idx + offset) % 7] }</span>
                {/each}
                {#each { length:6 } as w,idxw (idxw)}
                    {#if current[idxw]}
                        {#each { length:7 } as d,idxd (idxd)}
                            {#if current[idxw][idxd] != 0}
                            <div class:calnder-char-today="{isToday(current[idxw][idxd])}" 
                                    class="date calnder-chart tooltip">
                                { current[idxw][idxd] }
                                {#if report[current[idxw][idxd]]}
                                    {#if report[current[idxw][idxd]].total <= 5}
                                        <span class="bill bill-contrib bill-5"></span>
                                    {:else if report[current[idxw][idxd]].total > 5 && report[current[idxw][idxd]].total < 15}
                                        <span class="bill bill-contrib bill-10"></span>
                                    {:else if report[current[idxw][idxd]].total > 15}
                                        <span class="bill bill-contrib bill-15"></span>
                                    {/if}
                                    <div class="tooltiptext calnder-chart-bg calnder-chart">
                                        <div class="text-muted">
                                            <span class="float-left">
                                                Total
                                            </span>
                                            <span class="float-right">
                                                {report[current[idxw][idxd]].total}
                                            </span>
                                            <div class="row pr-0 row-hover">
                                                <div class="col">
                                                    <span class="bill bill-report-hover hover-pass pass"></span>
                                                </div>
                                                <div class="col">
                                                    <span class="bill bill-report-hover hover-skip skip"></span>
                                                </div>
                                                <div class="col">
                                                    <span class="bill bill-report-hover hover-fail fail"></span>
                                                </div>
                                            </div>
                                            <div class="row pr-0 row-hover">
                                                <div class="col">
                                                    <span class="report-text">{report[current[idxw][idxd]].passed}</span>
                                                </div>
                                                <div class="col">
                                                    <span class="report-text">{report[current[idxw][idxd]].skipped}</span>
                                                </div>
                                                <div class="col">
                                                    <span class="report-text">{report[current[idxw][idxd]].failed}</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                {/if}
                            </div>
                            {:else if (idxw < 1)}
                                <span class="date other">{ prev[prev.length - 1][idxd] }</span>
                            {:else}
                                <span class="date other">{ next[0][idxd] }</span>
                            {/if}
                        {/each}
                    {/if}
                {/each}
            </div>
        </div>
        <div class="card mt-4 p-3">
            <span class="text-muted">
                Hover on the day that contains dots to know the report of the day.
            </span>
            <div class="row mt-2">
                <div class="col-1 mt-2" style="width: 10px;">
                    <span class="bill bill-5"></span>
                </div>
                <div class="col-6 text-muted">
                    From 1 to 5 test cases run in the day.
                </div>
            </div>
            <div class="row">
                <div class="col-1 mt-2" style="width: 10px;">
                    <span class="bill bill-10"></span>
                </div>
                <div class="col-6 text-muted">
                    From 5 to 15.
                </div>
            </div>
            <div class="row">
                <div class="col-1 mt-2" style="width: 10px;">
                    <span class="bill bill-15"></span>
                </div>
                <div class="col-6 text-muted">
                    More than 15.
                </div>
            </div>
            <div class="row">
                <div class="col-1 mt-2" style="width: 10px;">
                    <span class="bill bill-today"></span>
                </div>
                <div class="col-6 text-muted">
                    Today hint.
                </div>
            </div>
        </div>
    </div>
{/if}
<svelte:head>
    <style>
        .month {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            text-align: right;
            grid-gap: 4px;
        }
        
        .label {
            font-weight: 300;
            text-align: center;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            opacity: 0.6;
        }
        
        .date {
            height: 50px;
            font-size: 16px;
            letter-spacing: -1px;
            padding-right: 4px;
            font-weight: 700;
            padding: 0.5rem;
            text-align: center;
        }
        
        .today {
            bottom: 4px;
            left: 18px;
        }
        .bill-contrib{
            bottom: 4px;
            left: 4px;
        }
        .date.other {
            opacity: 0.2;
        }
        .bill{
            display: block;
            position: absolute;
            padding: 5px;
            border-radius: 50%;
        }
        .bill-report-hover{
            bottom: 17px;
        }
        .tooltip {
            position: relative;
            display: inline-block;
            opacity: 2;
        }

        .tooltip .tooltiptext {
            visibility: hidden;
            text-align: left;
            width: 100%;
            position: absolute;
            z-index: 999;
            top: 0px;
            left: 0px;
            padding-left: 5px;
            height: 50px;
        }

        .tooltip:hover .tooltiptext {
            visibility: visible;
        }
        .float-right{
            float: right;
            padding-right: 8px;
            padding-top: 3px;
            font-size: 13px;
        }
        .float-left{
            font-size: 13px;
        }
        .row-hover{
            padding-left: 5px;
        }
        .col-pl-5{
            padding-left: 5px
        }
        .report-text{
            bottom: -2px;
            position: absolute;
            font-size: 12px;
            margin-left: 1px;
        }
    </style>
</svelte:head>
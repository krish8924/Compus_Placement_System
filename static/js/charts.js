// Charts.js for Campus Placement System
// This file contains chart initialization and configuration functions

document.addEventListener('DOMContentLoaded', function() {
    // Define color palette
    const colorPalette = {
        primary: '#0d6efd',
        secondary: '#6c757d',
        success: '#28a745',
        danger: '#dc3545',
        warning: '#ffc107',
        info: '#17a2b8',
        light: '#f8f9fa',
        dark: '#343a40',
        primaryLight: 'rgba(13, 110, 253, 0.2)',
        successLight: 'rgba(40, 167, 69, 0.2)',
        dangerLight: 'rgba(220, 53, 69, 0.2)',
        warningLight: 'rgba(255, 193, 7, 0.2)',
        infoLight: 'rgba(23, 162, 184, 0.2)'
    };

    // Common chart options
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        }
    };

    // Initialize charts if elements exist
    initializeCharts();

    // Function to initialize all charts
    function initializeCharts() {
        // Application Status Chart
        initializeApplicationStatusChart();
        
        // Department Placement Rate Chart
        initializePlacementRateChart();
        
        // Job Type Distribution Chart
        initializeJobTypeChart();
        
        // Monthly Job Postings Chart
        initializeMonthlyJobsChart();
    }

    // Application Status Distribution Chart
    function initializeApplicationStatusChart() {
        const applicationStatusChart = document.getElementById('applicationStatusChart');
        if (!applicationStatusChart) return;

        const ctx = applicationStatusChart.getContext('2d');
        
        // Data will be populated from the template
        // This is just a placeholder for demonstration
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Applied', 'Under Review', 'Shortlisted', 'Selected', 'Rejected'],
                datasets: [{
                    data: [30, 20, 15, 25, 10], // Will be overridden by template data
                    backgroundColor: [
                        colorPalette.primary,
                        colorPalette.info,
                        colorPalette.warning,
                        colorPalette.success,
                        colorPalette.danger
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions
            }
        });
    }

    // Department Placement Rate Chart
    function initializePlacementRateChart() {
        const placementRateChart = document.getElementById('placementRateChart');
        if (!placementRateChart) return;

        const ctx = placementRateChart.getContext('2d');
        
        // Data will be populated from the template
        new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering'],
                datasets: [{
                    label: 'Placement Rate (%)',
                    data: [92, 85, 78, 65], // Will be overridden by template data
                    backgroundColor: colorPalette.successLight,
                    borderColor: colorPalette.success,
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true,
                            max: 100
                        }
                    }]
                }
            }
        });
    }

    // Job Type Distribution Chart
    function initializeJobTypeChart() {
        const jobTypeChart = document.getElementById('jobTypeChart');
        if (!jobTypeChart) return;

        const ctx = jobTypeChart.getContext('2d');
        
        // Data will be populated from the template
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Full Time', 'Internship', 'Part Time'],
                datasets: [{
                    data: [65, 30, 5], // Will be overridden by template data
                    backgroundColor: [
                        colorPalette.primary,
                        colorPalette.warning,
                        colorPalette.info
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions
            }
        });
    }

    // Monthly Job Postings Chart
    function initializeMonthlyJobsChart() {
        const monthlyJobsChart = document.getElementById('monthlyJobsChart');
        if (!monthlyJobsChart) return;

        const ctx = monthlyJobsChart.getContext('2d');
        
        // Data will be populated from the template
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [{
                    label: 'Job Postings',
                    data: [12, 19, 3, 5, 2, 3, 7, 8, 12, 15, 10, 6], // Will be overridden by template data
                    backgroundColor: colorPalette.primaryLight,
                    borderColor: colorPalette.primary,
                    borderWidth: 2,
                    pointBackgroundColor: colorPalette.primary,
                    tension: 0.4
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            stepSize: 5
                        }
                    }]
                }
            }
        });
    }

    // Gender Distribution Chart (for officer dashboards)
    function initializeGenderDistributionChart(elementId, maleCount, femaleCount, otherCount) {
        const chartElement = document.getElementById(elementId);
        if (!chartElement) return;

        const ctx = chartElement.getContext('2d');
        
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Male', 'Female', 'Other'],
                datasets: [{
                    data: [maleCount, femaleCount, otherCount],
                    backgroundColor: [
                        colorPalette.primary,
                        colorPalette.danger,
                        colorPalette.warning
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions
            }
        });
    }

    // Salary Range Chart
    function initializeSalaryRangeChart(elementId, labels, data) {
        const chartElement = document.getElementById(elementId);
        if (!chartElement) return;

        const ctx = chartElement.getContext('2d');
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Offers',
                    data: data,
                    backgroundColor: colorPalette.successLight,
                    borderColor: colorPalette.success,
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1
                        }
                    }]
                }
            }
        });
    }

    // Custom chart function (to be used for custom charts)
    function createCustomChart(elementId, type, labels, datasets, options = {}) {
        const chartElement = document.getElementById(elementId);
        if (!chartElement) return;

        const ctx = chartElement.getContext('2d');
        
        const chartOptions = {
            ...commonOptions,
            ...options
        };
        
        new Chart(ctx, {
            type: type,
            data: {
                labels: labels,
                datasets: datasets
            },
            options: chartOptions
        });
    }

    // Export functions for external use
    window.chartFunctions = {
        initializeGenderDistributionChart,
        initializeSalaryRangeChart,
        createCustomChart
    };
});

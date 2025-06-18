$(document).ready(function () {
    function downloadReport() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#order-overview .start_date').val();
        var endDate = $('#order-overview .end_date').val();

        $.ajax({
            url: '/admin/api/download-order-report/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function (blob) {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.href = url;
                a.download = "orders_report_" + startDate.replaceAll('/', '-') + "_to_" + endDate.replaceAll('/', '-') + ".xlsx";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            },
            error: function (xhr, status, error) {
                console.error('Error downloading the report:', error);
            }
        });
    }

    $('#order-overview-download').click(function (e) {
        e.preventDefault();
        downloadReport();
    });

    // Thêm function download PDF tổng hợp
    function downloadOverallPDFReport() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#order-overview .start_date').val();
        var endDate = $('#order-overview .end_date').val();

        $.ajax({
            url: '/admin/api/download-overall-pdf-report/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function (blob) {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.href = url;
                a.download = "bao_cao_tong_hop_" + startDate.replaceAll('/', '-') + "_to_" + endDate.replaceAll('/', '-') + ".pdf";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            },
            error: function (xhr, status, error) {
                console.error('Error downloading the PDF report:', error);
            }
        });
    }

    // Thêm event listener cho nút download PDF
    $('#order-overview-download-pdf').click(function (e) {
        e.preventDefault();
        downloadOverallPDFReport();
    });

    function downloadReportPurchasebyCity() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#analytics-country .start_date').val();
        var endDate = $('#analytics-country .end_date').val();

        $.ajax({
            url: '/admin/api/download-export_payments/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function (blob) {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.href = url;
                a.download = "Revenue_report_" + startDate.replaceAll('/', '-') + "_to_" + endDate.replaceAll('/', '-') + ".xlsx"; // Sửa đổi định dạng tên file
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            },
            error: function (xhr, status, error) {
                console.error('Error downloading the report:', error);
            }
        });
    }

    $('.purchase-by-city').click(function (e) {
        e.preventDefault();
        downloadReportPurchasebyCity();
    });

});

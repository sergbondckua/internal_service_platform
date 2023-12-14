// Autocomplete
$(function () {
    $("#id_street_name").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/street_autocomplete",
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function (data) {
                    response($.map(data, function (item) {
                        return {
                            label: item.named,
                            value: item.named,
                            street_id: item.street_id
                        };
                    }));
                }
            });
        },
        minLength: 2, // Minimum characters before triggering autocomplete
        select: function (event, ui) {
            // Set the selected street_id to #id_num_street
            $("#id_street_id").val(ui.item.street_id);
            // Activate the house number filter for the selected street
            enableBuildingNumberFilter(ui.item.street_id);
        }
    });

    // Function for activating the house number filter
    function enableBuildingNumberFilter(streetId) {
        const buildingNumberSelect = $("#id_building_number");

        // Clear the building_number field
        buildingNumberSelect.empty();

        // Adding an empty element to the beginning of the list
        buildingNumberSelect.append('<option value="" selected disabled>Номер</option>');

        // Fill select with house numbers
        $.ajax({
            url: "/building_autocomplete",
            dataType: "json",
            data: {
                street_id: streetId
            },
            success: function (data) {
                // Adding each house number to the list
                $.each(data, function (index, item) {
                    buildingNumberSelect.append('<option value="' + item.building_number + '">' + item.building_number + '</option>');
                });

                // Enable "id_building_number" field
                buildingNumberSelect.prop('disabled', false);
            }
        });
    }
});

// Function to clear the contents of the input field with id "id_street_name" and
// "id_building_number" and blocking "id_building_number"
function clearInput() {
    document.getElementById("id_street_name").value = "";
    document.getElementById("id_building_number").value = "";
    document.getElementById("id_building_number").disabled = true;
}

// Modal dialog box search key
$(function () {
    $("#dialog-search-result").dialog({
        modal: true,
        autoOpen: true,
        height: "auto",
        width: "auto",
        resizable: true,
        show: {
            effect: "fade",
            duration: 1000
        },
        hide: {
            effect: "fade",
            duration: 500
        },
        buttons: [
            {
                text: "Дякую",
                icon: "",
                click: function () {
                    $(this).dialog("close");
                },
            }
        ],
    });
});
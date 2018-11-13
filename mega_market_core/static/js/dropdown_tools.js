function filling_filter_options(some_category_subcategory_item_filter_data, geo_filter_data, target_user_filter_data) {
    filling_category_subcategory_item_filter_options(some_category_subcategory_item_filter_data)
    filling_geo_filter_options(geo_filter_data)
    filling_target_user_filter_options(target_user_filter_data)
}


function filling_partially_category_subcategory_item_filter_options(category_subcategory_item_object) {

    if (category_subcategory_item_object.hasOwnProperty('subcategories')) {
        let category_list = categories_subcategories_items_filter_data
        for (let i = 0; i < category_list.length; i++) {
            let category = category_list[i]
            $('#categories').append('<option value=' + category.id + '>' + category.name + '</option>');
        }
        $('#categories').val(category_subcategory_item_object.id)

        let subcategory_list = category_subcategory_item_object.subcategories
        for (let i = 0; i < subcategory_list.length; i++) {
            let subcategory = subcategory_list[i]
            $('#subcategories').append('<option value=' + subcategory.id + '>' + subcategory.name + '</option>');
            items_list = subcategory.items
            for (let j = 0; j < items_list.length; j++) {
                let item = items_list[j]
                $('#items').append('<option value=' + item.id + '>' + item.name + '</option>');
            }
        }
    }
    else if (category_subcategory_item_object.hasOwnProperty('items')) {
        let parent_category = find_category_subcategory_or_item_parent(category_subcategory_item_object.id, 'subcategory')
        $('#categories').append('<option value=' + parent_category.id + '>' + parent_category.name + '</option>');
        $('#categories').val(parent_category.id)

        for (let i = 0; i < categories_subcategories_items_filter_data.length; i++) {
            let category = categories_subcategories_items_filter_data[i]
            let subcategory_list = category.subcategories

            for (let i = 0; i < subcategory_list.length; i++) {
                let subcategory = subcategory_list[i]
                $('#subcategories').append('<option value=' + subcategory.id + '>' + subcategory.name + '</option>');
            }
            $('#subcategories').val(category_subcategory_item_object.id)
        }

        let items_list = category_subcategory_item_object.items
        for (let j = 0; j < items_list.length; j++) {
            let item = items_list[j]
            $('#items').append('<option value=' + item.id + '>' + item.name + '</option>');
        }
    }
    else {
        let parent_subcategory = find_category_subcategory_or_item_parent(category_subcategory_item_object.id, 'item')
        $('#subcategories').append('<option value=' + parent_subcategory.id + '>' + parent_subcategory.name + '</option>');
        $('#subcategories').val(parent_subcategory.id)


        let parent_category = find_category_subcategory_or_item_parent(parent_subcategory.id, 'subcategory')
        $('#categories').append('<option value=' + parent_category.id + '>' + parent_category.name + '</option>');
        $('#categories').val(parent_category.id)

        for (let i = 0; i < categories_subcategories_items_filter_data.length; i++) {
            let category = categories_subcategories_items_filter_data[i]
            let subcategory_list = category.subcategories

            for (let j = 0; j < subcategory_list.length; j++) {
                let subcategory = subcategory_list[j]
                let item_list = subcategory.items
                for (let k = 0; k < item_list.length; k++) {
                    let item = item_list[k]
                    $('#items').append('<option value=' + item.id + '>' + item.name + '</option>');
                }
            }
        }
        $('#items').val(category_subcategory_item_object.id)
    }
}


function filling_category_subcategory_item_filter_options(some_category_subcategory_item_filter_data) {

    for (let i = 0; i < some_category_subcategory_item_filter_data.length; i++) {

        let subcategory_list = []
        let items_list = []

        if (some_category_subcategory_item_filter_data[i].hasOwnProperty('subcategories')) {
            let category = some_category_subcategory_item_filter_data[i]

            $('#categories').append('<option value=' + category.id + '>' + category.name + '</option>');
            subcategory_list = category.subcategories
        }
        //if it hasn't a subcategory list then it isn't a category so its given to the next fase in the subcategory_list
        else {
            subcategory_list = [some_category_subcategory_item_filter_data[i],]
        }


        for (let i = 0; i < subcategory_list.length; i++) {

            if (subcategory_list[i].hasOwnProperty('items')) {
                let subcategory = subcategory_list[i]

                $('#subcategories').append('<option value=' + subcategory.id + '>' + subcategory.name + '</option>');
                items_list = subcategory.items

                if ($('#categories')[0].value == "") {
                    let parent_category = find_category_subcategory_or_item_parent(subcategory_list[i].id, "subcategory")
                    $('#categories').append('<option value=' + parent_category.id + '>' + parent_category.name + '</option>');
                }
            }
            //if it hasn't an item list then it isn't a subcategory so its given to the next fase in the subcategory_list
            else {
                items_list = [subcategory_list[i],]
            }

            for (let i = 0; i < items_list.length; i++) {
                let item = items_list[i]

                $('#items').append('<option value=' + item.id + '>' + item.name + '</option>');

                if ($('#subcategories')[0].value == "") {
                    let parent_subcategory = find_category_subcategory_or_item_parent(item.id, "item")
                    $('#subcategories').append('<option value=' + parent_subcategory.id + '>' + parent_subcategory.name + '</option>');
                    if ($('#categories')[0].value == "") {
                        let parent_category = find_category_subcategory_or_item_parent(parent_subcategory.id, "subcategory")
                        $('#categories').append('<option value=' + parent_category.id + '>' + parent_category.name + '</option>');
                    }
                }
            }
        }
    }
}


function filling_geo_filter_options(geo_filter_data) {

    for (let i = 0; i < geo_filter_data.length; i++) {
        let geo = geo_filter_data[i]

        $('#geos').append('<option value=' + geo.id + '>' + geo.city_and_country + '</option>');
    }
}


function filling_target_user_filter_options(target_user_filter_data) {

    for (let i = 0; i < target_user_filter_data.length; i++) {
        let target_user = target_user_filter_data[i]

        $('#target_users').append('<option value=' + target_user.id + '>' + target_user.name + '</option>');
    }
}


function refresh_chart(chart_date_format) {

    console.log('Refreshing charts!')
    let filters_to_apply = {}

    if ($('#categories')[0].value != -1) {
        filters_to_apply.item__sub_category__category_id = $('#categories')[0].value
        if ($('#subcategories')[0].value != -1) {
            filters_to_apply.item__sub_category_id = $('#subcategories')[0].value
            if ($('#items')[0].value != -1) {
                filters_to_apply.item_id = $('#items')[0].value
            }
        }
    }

    if ($('#geos')[0].value != -1) {
        filters_to_apply.geo_id = $('#geos')[0].value
    }
    if ($('#target_users')[0].value != -1) {
        filters_to_apply.target_user_id = $('#target_users')[0].value
    }

    if ($('#date_options')[0].value == "custom_range") {
        let today_date = new Date()

        if ($('#start_date')[0].value == $('#end_date')[0].value) {
            filters_to_apply.date = $('#start_date')[0].value
        }
        else if ($('#start_date')[0].value != "" && $('#end_date')[0].value != "") {
            filters_to_apply.date__gt = $('#start_date')[0].value
            filters_to_apply.date__lt = $('#end_date')[0].value
        }
        else {
            let today_date = new Date()
            filters_to_apply.date__gt = today_date.toISOString().slice(0, 10)
            filters_to_apply.date__lt = today_date.addYears(-1).toISOString().slice(0, 10)

            $('#start_date')[0].value = filters_to_apply.date__gt
            $('#end_date')[0].value = filters_to_apply.date__lt
        }

        $('#date_range')[0].hidden = false
    }
    else {
        $('#date_range')[0].hidden = true
        if ($('#date_options')[0].value == "last_year") {
            let today_date = new Date()
            filters_to_apply.date__lt = today_date.toISOString().slice(0, 10)
            filters_to_apply.date__gt = today_date.addYears(-1).toISOString().slice(0, 10)
        }
        else if ($('#date_options')[0].value == "last_month") {
            let today_date = new Date()
            filters_to_apply.date__lt = today_date.toISOString().slice(0, 10)
            filters_to_apply.date__gt = today_date.addMonths(-1).toISOString().slice(0, 10)
        }
        else if ($('#date_options')[0].value == "yesterday") {
            let today_date = new Date()
            filters_to_apply.date = today_date.addDays(-1).toISOString().slice(0, 10)
        }
    }


    chart_tools(filters_to_apply)
}


function category_subcategory_item_refresh_chart(event) {

    if (event.currentTarget.id == 'categories') {
        object_type = 'category'
    }
    else if (event.currentTarget.id == 'subcategories') {
        object_type = 'subcategory'
    }
    else if (event.currentTarget.id == 'items') {
        object_type = 'item'
    }
    else {
        return ('unidentifyed type')
    }

    let object_id = event.currentTarget.value

    $('#categories').empty();
    $('#subcategories').empty();
    $('#items').empty();

    if (object_id == -1) {
        $('#categories').append('<option value="-1">All</option>');
        $('#subcategories').append('<option value="-1">All</option>');
        $('#items').append('<option value="-1">All</option>');
        filling_category_subcategory_item_filter_options(categories_subcategories_items_filter_data)
    }
    else {
        let selected_object_data = find_category_subcategory_or_item(object_id, object_type)

        if (object_type == 'category') {
            $('#categories').append('<option value="-1">All</option>');
            $('#subcategories').append('<option value="-1">All</option>');
            $('#items').append('<option value="-1">All</option>');
            filling_partially_category_subcategory_item_filter_options(selected_object_data)
        }
        else if (object_type == 'subcategory') {
            $('#categories').append('<option value="-1">All</option>');
            $('#subcategories').append('<option value="-1">All</option>');
            $('#items').append('<option value="-1">All</option>');
            filling_partially_category_subcategory_item_filter_options(selected_object_data)

            $('#subcategories')[0].value = object_id
        }
        else if (event.currentTarget.id == 'items') {
            $('#categories').append('<option value="-1">All</option>');
            $('#subcategories').append('<option value="-1">All</option>');
            $('#items').append('<option value="-1">All</option>');
            filling_partially_category_subcategory_item_filter_options(selected_object_data)
        }
        else {
            return ('unidentifyed type')
        }
    }

    refresh_chart(chart_date_format)
}


function draw_data_range_inputs() {
    let today_date = new Date()

    let date__lt = today_date.toISOString().slice(0, 10)
    let date__gt = today_date.addMonths(-1).toISOString().slice(0, 10)

    $('#date-range-inputs').append(
        '<div id="date_range">' +
        '    <div>\n' +
        '        <label for="start_date">Start</label>\n' +
        '        <input type="date" id="start_date" name="trip" class="form-control input-sm"\n' +
        '               value="' + date__gt + '"\n' +
        '               min="0001-01-01" max="\' + today_date + \'" />\n' +
        '    </div>\n' +
        '    <div>\n' +
        '        <label for="end_date">End</label>\n' +
        '        <input type="date" id="end_date" name="trip" class="form-control input-sm"\n' +
        '               value="' + date__lt + '"\n' +
        '               min="0001-01-01" max="' + today_date + '" />\n' +
        '    </div>\n' +
        '</div>');


    $('#date_range')[0].hidden = true
}

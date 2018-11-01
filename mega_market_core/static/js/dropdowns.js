function change_sub_category() {
    category_id = $('#categories').value

}

function refresh_chart() {
    let filters_to_apply = {
        // csrfmiddlewaretoken: '{{ csrf_token }}',
        date__lt: '2000-2-29',
        date__gt: '2000-2-1',
        // item_id: 3,
        // target_user_id: 1,
        geo_id: 1,
    }
    bought_chart(chart_date_format, filters_to_apply)
}


function filling_filter_options_backup2(full_category_filter_data, geo_filter_data, target_user_filter_data) {
    for (let i = 0; i < full_category_filter_data.length; i++) {

        let category = full_category_filter_data[i]
        $('#categories').append('<option value=' + category.id + '>' + category.name + '</option>');

        for (let i = 0; i < category.subcategories.length; i++) {
            let subcategory = category.subcategories[i]

            $('#subcategories').append('<option value=' + subcategory.id + '>' + subcategory.name + '</option>');

            for (let i = 0; i < subcategory.items.length; i++) {
                let item = subcategory.items[i]

                $('#items').append('<option value=' + item.id + '>' + item.name + '</option>');
            }
        }
    }

    for (let i = 0; i < geo_filter_data.length; i++) {
        let geo = geo_filter_data[i]

        $('#geos').append('<option value=' + geo.id + '>' + geo.city_and_country + '</option>');
    }
    for (let i = 0; i < target_user_filter_data.length; i++) {
        let target_user = target_user_filter_data[i]

        $('#target_users').append('<option value=' + target_user.id + '>' + target_user.name + '</option>');
    }
}

function filling_filter_options_backup(some_category_subcategory_item_filter_data, geo_filter_data, target_user_filter_data) {
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
            }
            //if it hasn't an item list then it isn't a subcategory so its given to the next fase in the subcategory_list
            else {
                items_list = [subcategory_list[i],]
            }

            for (let i = 0; i < items_list.length; i++) {
                let item = items_list[i]

                $('#items').append('<option value=' + item.id + '>' + item.name + '</option>');
            }
        }
    }

    for (let i = 0; i < geo_filter_data.length; i++) {
        let geo = geo_filter_data[i]

        $('#geos').append('<option value=' + geo.id + '>' + geo.city_and_country + '</option>');
    }
    for (let i = 0; i < target_user_filter_data.length; i++) {
        let target_user = target_user_filter_data[i]

        $('#target_users').append('<option value=' + target_user.id + '>' + target_user.name + '</option>');
    }
}

function filling_filter_options(some_category_subcategory_item_filter_data, geo_filter_data, target_user_filter_data) {
    filling_category_subcategory_item_filter_options(some_category_subcategory_item_filter_data)
    filling_geo_filter_options(geo_filter_data)
    filling_target_user_filter_options(target_user_filter_data)
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
                
                if ($('#categories')[0].value == ""){
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

                if ($('#subcategories')[0].value == ""){
                    let parent_subcategory = find_category_subcategory_or_item_parent(item.id, "item")
                    $('#subcategories').append('<option value=' + parent_subcategory.id + '>' + parent_subcategory.name + '</option>');
                    if ($('#categories')[0].value == ""){
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


function find_category_subcategory_or_item(id, type) {

    let all_categories = categories_subcategories_items_filter_data

    for (let i = 0; i < all_categories.length; i++) {
        if (type == 'category') {
            if (all_categories[i].id == id) {
                let to_return = all_categories[i]
                return to_return
            }
        }
        else {
            let subcategories = all_categories[i].subcategories

            for (let j = 0; j < subcategories.length; j++) {
                if (type == 'subcategory') {
                    if (subcategories[j].id == id) {

                        let to_return = subcategories[j]
                        to_return.category_id = all_categories[i].id
                        return to_return
                    }
                }
                else {
                    let items = subcategories[j].items

                    for (let k = 0; k < items.length; k++) {
                        if (items[k].id == id) {
                            let to_return = items[k]
                            to_return.subcategory_id =subcategories[j].id
                            to_return.category_id = all_categories[i].id
                            return to_return
                            return items[k]
                        }
                    }
                }
            }
        }
    }
    return 'Nothing was found with this parameters'
}


function find_category_subcategory_or_item_parent(id, type) {

    let all_categories = categories_subcategories_items_filter_data

    for (let i = 0; i < all_categories.length; i++) {
        if (type == 'category') {
            if (all_categories[i].id == id) {
                let to_return = all_categories[i]
                return 'i`m a campaign'
            }
        }
        else {
            let subcategories = all_categories[i].subcategories

            for (let j = 0; j < subcategories.length; j++) {
                if (type == 'subcategory') {
                    if (subcategories[j].id == id) {
                        let to_return = all_categories[i]
                        return to_return
                    }
                }
                else {
                    let items = subcategories[j].items

                    for (let k = 0; k < items.length; k++) {
                        if (items[k].id == id) {
                            let to_return = subcategories[j]
                            to_return.category_id = all_categories[i].id
                            return to_return
                        }
                    }
                }
            }
        }
    }
    return 'Nothing was found with this parameters'
}


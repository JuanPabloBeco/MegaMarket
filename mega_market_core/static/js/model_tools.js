
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
                            to_return.subcategory_id = subcategories[j].id
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
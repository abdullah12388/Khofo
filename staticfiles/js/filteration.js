var sub_category_id = document.getElementById('sub_category_id');
var filtering_parent = document.getElementById('filtering');
var langCode = document.getElementById('langCode');
var list_dict = [];
for (var i = 0; i < filtering_parent.children.length; i++) {
    small_parents(i)
}

function small_parents(x) {
    var spec_name = filtering_parent.children[x].children[0].children[0];
    for (var i = 2; i < spec_name.children.length; i++) actions(x, i)
}

function actions(parent, small_parent) {
    var spec_values_input = filtering_parent.children[parent].children[0].children[0].children[small_parent].children[0];
    console.log("parent = " + parent);
    console.log("small_parent = " + small_parent);
    spec_values_input.onchange = function () {
        if (spec_values_input.checked) {
            var spec_name = filtering_parent.children[parent].children[0].children[0].children[1];
            var spec_values = filtering_parent.children[parent].children[0].children[0].children[small_parent].children[1];
            console.log("spec_name = " + spec_name.innerHTML);
            console.log("spec_values = " + spec_values.innerHTML);
            var obj = {"spec_name": spec_name.innerHTML, "spec_value": spec_values.innerHTML};
            list_dict.push(obj);
            $.ajax({
                type: 'GET',
                url: "/productHome/ajax/check_filter/",
                traditional: true,
                data: {
                    sub_category_id: sub_category_id.innerText,
                    spec_name: spec_name.innerHTML,
                    spec_value: spec_values.innerHTML,
                    lang_code: langCode.innerHTML,
                },
                dataType: 'json',
                contentType: 'application/json; charset=utf-8',
                success: function (data) {
                    if (data.done) {
                        for (var i = 0; i < filtering_parent.children.length; i++) {
                            small_parents_(i)
                        }

                        function small_parents_(x) {
                            var spec_name_ = filtering_parent.children[x].children[0].children[0];
                            for (var i = 2; i < spec_name_.children.length; i++) actions_(x, i)
                        }

                        function actions_(parent, small_parent) {
                            var spec_values_input_ = filtering_parent.children[parent].children[0].children[0].children[small_parent].children[0];
                            spec_values_input_.disabled = true;
                            spec_values_input_.nextElementSibling.classList.add('line-through')
                        }

                        var spec_values_values = data.spec_values_values;
                        console.log("spec_values_values = " + spec_values_values);
                        for (var indexi = 0; indexi < spec_values_values.length; indexi++) {
                            var inputs_enable_ = document.getElementsByClassName('' + spec_values_values[indexi] + '')[0];
                            if (inputs_enable_ !== null) {
                                inputs_enable_.disabled = false;
                                inputs_enable_.nextElementSibling.classList.remove('line-through')
                            }
                        }
                    } else {
                        console.log("Error: ", data)
                    }
                }
            })
        } else {
            enble_all()
        }
    }
}

function enble_all() {
    var selection_choose = document.getElementById("selection_choose");
    selection_choose.classList.remove("btn-success");
    selection_choose.classList.add("btn-danger");
    $.ajax({
        type: 'GET',
        url: "/productHome/ajax/delete_selection/",
        traditional: true,
        data: {delete_item: 1},
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
        }
    });
    for (var i = 0; i < filtering_parent.children.length; i++) {
        small_parents_(i)
    }

    function small_parents_(x) {
        var spec_name_ = filtering_parent.children[x].children[0].children[0];
        for (var i = 2; i < spec_name_.children.length; i++) actions_(x, i)
    }

    function actions_(parent, small_parent) {
        var spec_values_input_1 = filtering_parent.children[parent].children[0].children[0].children[small_parent].children[0];
        spec_values_input_1.disabled = false;
        spec_values_input_1.checked = false;
        spec_values_input_1.nextElementSibling.classList.remove('line-through')
    }
}
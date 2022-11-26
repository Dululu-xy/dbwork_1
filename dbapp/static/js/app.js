$(document).ready(function () {
    var $wrapper = $('.main-wrapper');
    var $pageWrapper = $('.page-wrapper');
    var Sidemenu = function () {
        this.$menuItem = $('#sidebar-menu a');
    };
    function init() {
        var $this = Sidemenu;
        $('#sidebar-menu a').on('click',
        function (e) {
            if ($(this).parent().hasClass('submenu')) {
                e.preventDefault();
            }
            if (!$(this).hasClass('subdrop')) {
                $('ul', $(this).parents('ul:first')).slideUp(350);
                $('a', $(this).parents('ul:first')).removeClass('subdrop');
                $(this).next('ul').slideDown(350);
                $(this).addClass('subdrop');
            } else if ($(this).hasClass('subdrop')) {
                $(this).removeClass('subdrop');
                $(this).next('ul').slideUp(350);
            }
        });
        $('#sidebar-menu ul li.submenu a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
    }
    init();
    $('body').append('<div class="sidebar-overlay z-[1004] top-[60px] left-0 w-full h-full"></div>');
    $(document).on('click', '#mobile_btn',
    function () {
        $wrapper.toggleClass('slide-nav');
        $('.sidebar-overlay').toggleClass('opened bg-blackOverlay fixed');
        $('html').addClass('menu-opened');
        $('#task_window').removeClass('opened bg-blackOverlay');
        return false;
    });
    $(".sidebar-overlay").on("click",
    function () {
        $('html').removeClass('menu-opened');
        $(this).removeClass('opened');
        $wrapper.removeClass('slide-nav');
        $('.sidebar-overlay').removeClass('opened bg-blackOverlay fixed');
        $('#task_window').removeClass('opened bg-blackOverlay');
    });
    $(document).on('click', '#task_chat',
    function () {
        $('.sidebar-overlay').toggleClass('opened bg-blackOverlay fixed');
        $('#task_window').addClass('opened bg-blackOverlay');
        return false;
    });
    $(document).on('click', '#toggle_btn',
    function () {
        if ($('body').hasClass('mini-sidebar')) {
            $('body').removeClass('mini-sidebar');
            $('.subdrop + ul').slideDown();
        } else {
            $('body').addClass('mini-sidebar');
            $('.subdrop + ul').slideUp();
        }
        return false;
    });
    $(document).on('mouseover',
    function (e) {
        e.stopPropagation();
        if ($('body').hasClass('mini-sidebar') && $('#toggle_btn').is(':visible')) {
            var targ = $(e.target).closest('.sidebar').length;
            if (targ) {
                $('body').addClass('expand-menu');
                $('.subdrop + ul').slideDown();
            } else {
                $('body').removeClass('expand-menu');
                $('.subdrop + ul').slideUp();
            }
            return false;
        }
    });
    if ($('.datatable').length > 0) {
        $('.datatable').DataTable({
            "bFilter": false,
            responsive: true,
        });
    }
    $(document).on('click', '#task_complete',
    function () {
        $(this).toggleClass('task-completed');
        return false;
    });
    if ($('#customleave_select').length > 0) {
        $('#customleave_select').multiselect();
    }
    if ($('#edit_customleave_select').length > 0) {
        $('#edit_customleave_select').multiselect();
    }
    $(document).on('click', '.leave-edit-btn',
    function () {
        $(this).removeClass('leave-edit-btn').addClass('btn btn-white leave-cancel-btn').text('Cancel');
        $(this).closest("div.leave-right").append('<button class="btn btn-primary leave-save-btn" type="submit">Save</button>');
        $(this).parent().parent().find("input").prop('disabled', false);
        return false;
    });
    $(document).on('click', '.leave-cancel-btn',
    function () {
        $(this).removeClass('btn btn-white leave-cancel-btn').addClass('leave-edit-btn').text('Edit');
        $(this).closest("div.leave-right").find(".leave-save-btn").remove();
        $(this).parent().parent().find("input").prop('disabled', true);
        return false;
    });
    $(document).on('change', '.leave-box .onoffswitch-checkbox',
    function () {
        var id = $(this).attr('id').split('_')[1];
        if ($(this).prop("checked") == true) {
            $("#leave_" + id + " .leave-edit-btn").prop('disabled', false);
            $("#leave_" + id + " .leave-action .btn").prop('disabled', false);
        } else {
            $("#leave_" + id + " .leave-action .btn").prop('disabled', true);
            $("#leave_" + id + " .leave-cancel-btn").parent().parent().find("input").prop('disabled', true);
            $("#leave_" + id + " .leave-cancel-btn").closest("div.leave-right").find(".leave-save-btn").remove();
            $("#leave_" + id + " .leave-cancel-btn").removeClass('btn btn-white leave-cancel-btn').addClass('leave-edit-btn').text('Edit');
            $("#leave_" + id + " .leave-edit-btn").prop('disabled', true);
        }
    });
    $('.leave-box .onoffswitch-checkbox').each(function () {
        var id = $(this).attr('id').split('_')[1];
        if ($(this).prop("checked") == true) {
            $("#leave_" + id + " .leave-edit-btn").prop('disabled', false);
            $("#leave_" + id + " .leave-action .btn").prop('disabled', false);
        } else {
            $("#leave_" + id + " .leave-action .btn").prop('disabled', true);
            $("#leave_" + id + " .leave-cancel-btn").parent().parent().find("input").prop('disabled', true);
            $("#leave_" + id + " .leave-cancel-btn").closest("div.leave-right").find(".leave-save-btn").remove();
            $("#leave_" + id + " .leave-cancel-btn").removeClass('btn btn-white leave-cancel-btn').addClass('leave-edit-btn').text('Edit');
            $("#leave_" + id + " .leave-edit-btn").prop('disabled', true);
        }
    });
    $(document).on('click', '#file_sidebar_toggle',
    function () {
        $('.file-wrap').toggleClass('file-sidebar-toggle');
    });
    $(document).on('click', '.file-side-close',
    function () {
        $('.file-wrap').removeClass('file-sidebar-toggle');
    });
    if ($('.clickable-row').length > 0) {
        $(".clickable-row").click(function () {
            window.location = $(this).data("href");
        });
    }
    if ($('.summernote').length > 0) {
        $('.summernote').summernote({
            height: 200,
            minHeight: null,
            maxHeight: null,
            focus: false
        });
    }
    var pHeight = $(window).height();
    $pageWrapper.css('min-height', pHeight);
    $(window).resize(function () {
        var prHeight = $(window).height();
        $pageWrapper.css('min-height', prHeight);
    });
    if ($('.kanban-wrap').length > 0) {
        $(".kanban-wrap").sortable({
            connectWith: ".kanban-wrap",
            handle: ".kanban-box",
            placeholder: "drag-placeholder"
        });
    }
    $(function () {
        $(document).on("click", '.btn-add-row',
        function () {
            var id = $(this).closest("table.table-review").attr('id');
            console.log(id);
            var div = $("<tr />");
            div.html(GetDynamicTextBox(id));
            $("#" + id + "_tbody").append(div);
        });
        $(document).on("click", "#comments_remove",
        function () {
            $(this).closest("tr").prev().find('td:last-child').html('<button type="button" class="btn border-danger bg-danger text-white hover:bg-[#e6294b]" id="comments_remove"><i class="fa fa-trash-o"></i></button>');
            $(this).closest("tr").remove();
        });
        function GetDynamicTextBox(table_id) {
            $('#comments_remove').remove();
            var rowsLength = document.getElementById(table_id).getElementsByTagName("tbody")[0].getElementsByTagName("tr").length + 1;
            return '<td>' + rowsLength + '</td>' + '<td><input type="text" name = "DynamicTextBox" class="block w-full inputStyle" value = "" ></td>' + '<td><input type="text" name = "DynamicTextBox" class="block w-full inputStyle" value = "" ></td>' + '<td><input type="text" name = "DynamicTextBox" class="block w-full inputStyle" value = "" ></td>' + '<td><button type="button" class="btn border-danger bg-danger text-white hover:bg-[#e6294b]" id="comments_remove"><i class="fa fa-trash-o"></i></button></td>'
        }
    });
    $(document).ready(function () {
        $("#result b").html($("#customRange").val());
        $("#customRange").change(function () {
            $("#result b").html($(this).val());
        });
    });
});
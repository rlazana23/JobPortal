$(document).ready(function(){
    $('#post-job-btn').click(function(event){
        $('.company-form-post-job').hide();
        $('.company-form-cont').show();
    });
    $('#close-job-btn').click(function(event){
        $('.company-form-post-job').show();
        $('.company-form-cont').hide();
    });
    $('.banner-btn').click(function(event){
        $('.home-banner-container').hide();
    });
    $("#user-add-skill-button").click(function(event){
        event.preventDefault();
        
        $("#user-add-skill-form").show();
        $(this).hide();
    });

    $("#user-add-skill-cancel").click(function(event){
        event.preventDefault();
        $("#user-add-skill-form").hide();
        $("#user-add-skill-button").show();
    });

    $("#user-add-previous-work-button").click(function(event){
        event.preventDefault();
        
        $("#user-add-previous-work-form").show();
        $(this).hide();
    });

    $("#user-add-previous-work-cancel").click(function(event){
        event.preventDefault();
        $("#user-add-previous-work-form").hide();
        $("#user-add-previous-work-button").show();
    });
    $("#user-edit-profile-button").click(function(event){
        event.preventDefault();
        
        $("#user-edit-profile-form").show();
        $("#user-profile-personal-info").hide();
        $("#user-profile-personal-info").display(none);
        $(this).display(none);
        $(this).hide();
    });

    $("#user-edit-profile-cancel").click(function(event){
        event.preventDefault();
        $("#user-edit-profile-form").hide();
        $("#user-edit-profile-button").show();
        $("#user-profile-personal-info").show();
        $(this.hide)

    });
});

function confirmWorkDelete(id, name){
    Swal.fire({
        title: 'Are you sure you want to remove ' +name +"?",
        text: '',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed){
            window.location = "/removeWork/"+id;
        }
    })
}
function confirmSkillRemove(id,name){

    Swal.fire({
        title: 'Are you sure you want to remove ' +name +"?",
        text: '',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed){
            window.location = "/removeSkill/"+id;
        }
    })
}
function logout(){
Swal.fire({
        title: 'Are you sure you want to logout?',
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/logout'
        }
    })
};

function cancelApplication(){
    Swal.fire({
            title: 'Are you sure you want to cancel your application?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = "base/seeker_canceldelete_applications";
            }
        })
    };

function deleteJob(id){
Swal.fire({
        title: 'Are you sure you want to close posted job?',
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed){
            location.href = "/Delete/" + id;
        }
    })
};

function deleteAccount(){
    Swal.fire({
            title: 'Are you sure you want to delete your account?',
            text: "",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes'
        }).then((result) => {
            if (result.isConfirmed) {
                document.getElementById('deleteAccount').click();
                // location.href = "/company_delete_job" + id;
            }
        })
    };

function application(str){
    var t = ""
    if(str == "accept")
        t = "Accept this applicant?";
    else
        t = "Reject this applicant?";
Swal.fire({
        title: t,
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed) {
            if(str == "accept")
                document.getElementById('accept').click();
            else
            document.getElementById('reject').click();
            // location.href = "/company_delete_job" + id;
        }
    })
};

function userApplication(str){
    var t = ""
    if(str == "cancel")
        t = "Cancel this application?";
    else
        t = "Remove accepted application?";
Swal.fire({
        title: t,
        text: "",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed) {
            if(str == "cancel")
                document.getElementById('cancel').click();
            else
            document.getElementById('remove').click();
            // location.href = "/company_delete_job" + id;
        }
    })
};
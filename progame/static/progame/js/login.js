

// $("#signup").click(function() {
//     $("#login-entrar").fadeOut("fast", function() {
//         $("#login-criar").fadeIn("fast");
//     });
// });

// $("#signin").click(function() {
//     $("#login-criar").fadeOut("fast", function() {
//        $("#login-entrar").fadeIn("fast");
//     });
// });


  
// $("form[name='login']").submit(function() {
//     $("form[name='login']").validate({
//         rules: {
//             email: {
//                 required: true,
//                 email: true
//             },
//             password: {
//                 required: true,
//             }
//         },

//         messages: {
//             email: "Por favor, digite um endereço de email válido",
//             password: {
//                 required: "Por favor, digite uma senha válida",
//             }
//         },

//         submitHandler: function(form) {
//             form.submit();
//         }
//     });
// });
         


$(function() {
    $("form[name='resgistro']").validate({
        rules: {
            email: {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 5
            },
            confirm_password: {
                required: true,
                minlength: 5
            }
        },
    
        messages: {
            password: {
                required: "Por favor, digite uma senha",
                minlength: "Sua senha deve ter pelo menos 5 caracteres"
            },
            confirm_password: {
                required: "Por favor, digite uma senha",
                minlength: "Sua senha deve ter pelo menos 5 caracteres"
            },
            email: "Por favor, digite um endereço de email válido"
        },
  
        submitHandler: function(form) {
            form.submit();
        }
    });
});
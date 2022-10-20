document.getElementById('btnCadastraVenda').addEventListener('click', function(){
    alert('cliquei');

    $.ajax({
        data: {
            teste: 'passei'
        },
        type: 'POST',
        url: '/cadastrar_venda'
    })
    .done(function(data){
        /*
        if(data.error){
            console.log('erro ' + data.error);
        }
        else if(data){
            $("#cnpj").val(data.cnpj);
            $("#razaosocial").val(data.razaosocial);
            $("#cep").val(data.cep);
            $("#endereco").val(data.endereco);
            $("#numero_endereco").val(data.numero_endereco);
            $("#complemento").val(data.complemento);
            $("#cidade").val(data.cidade);
            $("#UF").val(data.uf);
            $("#nome_contato").val(data.nome_contato);
            $("#email").val(data.email);
            $("#telefone").val(data.telefone);
            $("#celular").val(data.celular);
            }
        */
    
    });
})


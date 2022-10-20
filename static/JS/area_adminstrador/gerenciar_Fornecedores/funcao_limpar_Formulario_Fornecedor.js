
// ################### LIMPAR A TABELA DEPOIS DE CLICK NO BOTÃO ADICIONAR #############

$("#limpar").click(function(){
    $("input[data-name='entrada']").val('');
  });

// Código para limpar formulario ao click no botão = https://pt.stackoverflow.com/questions/174194/como-limpar-input

// ################### FIM LIMPAR A TABELA DEPOIS DE CLICK NO BOTÃO ADICIONAR #############



// #########################################################################################
// ################## LIMPAR OS COMBOBOX DEPOIS DO CLICK NO BOTÃO ADICIONAR ###############

//                 UF do Usuario
$("#limpar").on("click", function () { // Nome do botão
  $("select.form-list-UF option").each(function(i){ // Classe do Select
      $(this).removeAttr("selected");
      if (i == 0) this.selected = true; // onde o "i" é o index desse select, começando em zero
    });
});

//                 Cargo do Funcionario
$("#limpar").on("click", function () { // Nome do botão
  $("select.form-list-Cargo option").each(function(i){ // Classe do Select
      $(this).removeAttr("selected");
      if (i == 0) this.selected = true; // onde o "i" é o index desse select, começando em zero
    });
});





// Código dessa função: http://jsfiddle.net/suhjnxaj/1/

// ################## FIM LIMPAR OS COMBO BOX DEPOIS DO CLICK NO BOTÃO ADICIONAR ###############



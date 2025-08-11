*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    String    # Para gerar logs mais informativos

Suite Setup     Inicializar Testes
Suite Teardown  Finalizar Testes
Test Timeout    60 minutes  # Tempo suficiente para todas as VLANs

*** Variables ***
${VLAN_INICIO}    2
${VLAN_FIM}       4094
${LOTE_SIZE}      100  # Número de VLANs por lote

*** Test Cases ***
Testar criação de todas as VLANs válidas
    [Template]    Criar VLAN e Validar
    FOR    ${vlan_id}    IN RANGE    ${VLAN_INICIO}    ${VLAN_FIM}+1
        ${vlan_id}
    END

*** Keywords ***
Inicializar Testes
    Create Session    api    http://api:5000    timeout=30
    Log    Iniciando teste de VLANs de ${VLAN_INICIO} a ${VLAN_FIM}    level=INFO

Finalizar Testes
    Delete All Sessions
    Log    Teste de VLANs concluído    level=INFO

Criar VLAN e Validar
    [Arguments]    ${vlan_id}
    ${payload}=    Create Dictionary    id=${vlan_id}    name=VLAN_${vlan_id}
    
    # Log de progresso a cada 100 VLANs
    Run Keyword If    ${vlan_id} % ${LOTE_SIZE} == 0
    ...    Log    Processando VLAN ${vlan_id} de ${VLAN_FIM}    level=INFO
    
    ${response}=    POST On Session    api    /vlans    json=${payload}
    
    # Verificação do status code
    Run Keyword If    ${response.status_code} == 201
    ...    Validar Resposta Criacao    ${response}    ${vlan_id}
    ...  ELSE IF    ${response.status_code} == 409
    ...    Log    VLAN ${vlan_id} já existe    level=WARN
    ...  ELSE
    ...    Fail    Erro inesperado na VLAN ${vlan_id}: ${response.status_code} - ${response.text}

Validar Resposta Criacao
    [Arguments]    ${response}    ${vlan_id}
    ${json}=    Set Variable    ${response.json()}
    
    # Validações principais
    Should Be Equal As Numbers    ${json['vlan']['id']}    ${vlan_id}
    Dictionary Should Contain Key    ${json['vlan']}    status
    Dictionary Should Contain Key    ${json['vlan']}    name
    Dictionary Should Contain Key    ${json['vlan']}    created_at
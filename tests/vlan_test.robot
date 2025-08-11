*** Settings ***
Library    RequestsLibrary
Library    Collections

Suite Setup     Create Session    api    http://api:5000
Suite Teardown  Delete All Sessions

*** Test Cases ***
Criar VLAN Válida
    ${headers}=    Create Dictionary    Content-Type=application/json
    ${data}=    Create Dictionary    id=100    name=VLAN_TESTE
    ${response}=    POST On Session    api    /vlans    json=${data}    headers=${headers}
    Status Should Be    201    ${response}
    Should Be Equal As Strings    ${response.json()['id']}    100
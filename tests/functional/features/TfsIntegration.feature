@jenkins
Feature: TFS entegrasyonu
    Scriptlerin tfs üzerinden alınıp deloy edilmesi

    # birkaç comment

    Scenario: son deploydan sonra ki scriplterin deployu
        Given tfsde "Katilim" üzerinde yetkili kullanıcı bağlantısı
        And son deployun changet idsini al # başlangıç id
        And tfs üzerinde ki max changeseti al # bitiş id
        And başlangıç id ve bitiş id arasında ki changeset listesini doldur
        When listede ki scriptler "Dev" ortamına ait olanlar tfs üzerinden indirilir
        Then "Dev" ortamda scriptler sqlplus ile db üzerinde execute edilir
        And sonuçlar loglanır
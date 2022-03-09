StoresComponent = {
    ext_lang: 'stores_code',
    formats: ['format_stores'],
    struct_support: true,
    concept_rating: 0,
    concept_hardware_store: 0,
    nrel_store_rating: 0,
    factory: function (sandbox) {
        return new StoresWindow(sandbox);
    }
};

StoresWindow = function (sandbox) {

    this.sandbox = sandbox;
    this.sandbox.container = sandbox.container;

    const keynodes = ['ui_stores_text_component', 'ui_stores_search_component', 'ui_stores_answer_button',
    'ui_stores_info_block', 'concept_rating', 'concept_hardware_store', 'nrel_store_rating'];
    const minRating = '#stores-' + sandbox.container + " #min-rating";
    const maxRating = '#stores-' + sandbox.container + " #max-rating";
    const answerButton = '#stores-' + sandbox.container + " #answer-button1";
    const infoBlock = '#stores-' + sandbox.container + " #info"

    $('#' + sandbox.container).prepend('<div id="stores-' + sandbox.container + '"></div>');

    $('#stores-' + sandbox.container).load('static/components/html/stores.html', function () {
        getUIComponentsIdentifiers();

        $(answerButton).click(function (event) {
            event.preventDefault();
            let minRatingValue = $(minRating).val();
            let maxRatingValue = $(maxRating).val();
            if (minRatingValue && maxRatingValue) {
                findStoresByRating(parseInt(minRatingValue), parseInt(maxRatingValue));
            }
        });
    });

    this.applyTranslation = function () {
        getUIComponentsIdentifiers();
    };

    function getUIComponentsIdentifiers() {
        SCWeb.core.Server.resolveScAddr(keynodes, function (keynodes) {
            SCWeb.core.Server.resolveIdentifiers(keynodes, function (identifiers) {
                let searchComponentScAddr = keynodes['ui_stores_search_component'];
                let searchComponentText = identifiers[searchComponentScAddr];
                $(answerButton).html(searchComponentText);
                $(answerButton).attr('sc_addr', searchComponentScAddr);
                StoresComponent.concept_rating = keynodes['concept_rating'];
                StoresComponent.concept_hardware_store = keynodes['concept_hardware_store'];
                StoresComponent.nrel_store_rating = keynodes['nrel_store_rating'];
            });
        });
    }

    function findStoresByRating(minRating, maxRating) {
        window.sctpClient.iterate_elements(SctpIteratorType.SCTP_ITERATOR_3F_A_A, [
            StoresComponent.concept_hardware_store,
            sc_type_arc_pos_const_perm,
            sc_type_node]).
            done(function(identifiers) {
                for (let i = 0; i < identifiers.length; ++i) {
                    let store = identifiers[i][2];
                    window.sctpClient.iterate_elements(SctpIteratorType.SCTP_ITERATOR_5F_A_A_A_F, [
                        identifiers[i][2],
                        sc_type_arc_common | sc_type_const,
                        sc_type_link,
                        sc_type_arc_pos_const_perm,
                        StoresComponent.nrel_store_rating
                    ]).done(function (identifiers) {
                        SCWeb.core.Server.resolveIdentifiers([identifiers[0][2], store], function (keynodes) {
                            window.sctpClient.get_link_content(identifiers[0][2], 'string').done(function (content) {
                                let rating = parseInt(content);
                                if (rating >= minRating && rating <= maxRating) {
                                    $('#info').html($('#info').html() + keynodes[store] + "<br/>");
                                }}); 
                            
                        });
                    });
                }
            });
    }
};

SCWeb.core.ComponentManager.appendComponentInitialize(StoresComponent);

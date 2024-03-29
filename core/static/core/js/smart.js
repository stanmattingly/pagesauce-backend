document.addEventListener('DOMContentLoaded', () => {
    const apiKey = document.querySelector('[data-smart-auth-id]').dataset.smartAuthId;
    const urlParams = new URLSearchParams(window.location.search);
    const smartAddToken = urlParams.get('smart-add-token');
    const xPaths = []
    const unprocessed = []
    const xPathComponentMapping = {}

    function isHTML(str) {
        var a = document.createElement('div');
        a.innerHTML = str;

        for (var c = a.childNodes, i = c.length; i--;) {
            if (c[i].nodeType == 1) return true;
        }

        return false;
    }

    function parentIsButtonOrLink(element) {
        return (element.parentElement.tagName === 'BUTTON' || element.parentElement.tagName === 'A');
    }

    function createXPathFromElement(elm) {
        var allNodes = document.getElementsByTagName('*');
        for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) {
            if (elm.hasAttribute('id')) {
                var uniqueIdCount = 0;
                for (var n = 0; n < allNodes.length; n++) {
                    if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++;
                    if (uniqueIdCount > 1) break;
                };
                if (uniqueIdCount == 1) {
                    segs.unshift('id("' + elm.getAttribute('id') + '")');
                    return segs.join('/');
                } else {
                    segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]');
                }
            } else if (elm.hasAttribute('class')) {
                segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]');
            } else {
                for (i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) {
                    if (sib.localName == elm.localName) i++;
                };
                segs.unshift(elm.localName.toLowerCase() + '[' + i + ']');
            };
        };
        return segs.length ? '/' + segs.join('/') : null;
    };

    function createSelectorFromElement(element){
        var names = [];
        while (element.parentNode){
          if (element.id){
            names.unshift('#'+element.id);
            break;
          }else{
            if (element==element.ownerDocument.documentElement) names.unshift(element.tagName);
            else{
              for (var c=1,e=element;e.previousElementSibling;e=e.previousElementSibling,c++);
              names.unshift(element.tagName+":nth-child("+c+")");
            }
            element=element.parentNode;
          }
        }
        return names.join(" > ");
      }

    function getElementByXpath(path, element=null) {
        if (element !== null) {
            return document.evaluate(path, element, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }
        return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }

    function getElementBySelector(selector, element=null) {
        if (element !== null) {
            return element.querySelector(selector)
        }

        return document.querySelector(selector)
    }

    function getElementCssText(element) {
        const styles = window.getComputedStyle(element);
        if (styles.cssText !== '') {
            return styles.cssText;
        } else {
            const cssText = Object.values(styles).reduce(
                (css, propertyName) =>
                    `${css}${propertyName}:${styles.getPropertyValue(
                        propertyName
                    )};`
            );
            return cssText;
        }
    }

    fetch(`https://api.pagesauce.io/auth/smart-add-tokens/${smartAddToken}/`, {
        method: "get",
        headers: {
            'Authorization': `Token ${apiKey}`,
        },
    }).then(response => {
        if (response.ok) {
            response.json().then(() => {
                document.addEventListener('click', function (event) {
                    // (note: not cross-browser)
                    if(!event.shiftKey) {
                        let smartClick = new CustomEvent('smartclick', {detail: {original: event}},);
                        document.dispatchEvent(smartClick);
                        event.stopPropagation();
                        event.preventDefault();
                    }

                    if (event.target.href ) {
                        if (!event.target.href.includes(smartAddToken)) {
                            let url = new URL(event.target.href)
                            url.searchParams.append('smart-add-token', smartAddToken)
                            event.target.href = url.href;
                        }
                    }

                    if (event.target.parentElement.href) {
                        if (!event.target.parentElement.href.includes(smartAddToken)) {
                            let url = new URL(event.target.parentElement.href)
                            url.searchParams.append('smart-add-token', smartAddToken)
                            event.target.parentElement.href = url.href;
                        }
                    }
                }, true);

                document.addEventListener('mouseover', event => {
                    const element = event.target

                    if (!isHTML(event.target.innerHTML) && event.target.innerHTML) {
                        element.style.cursor = "pointer";

                        if (!element.dataset.clicked) {
                            element.dataset.originalBorder = element.style.border;
                        }
                        if (!element.dataset.clicked) {
                            element.style.border = "2px solid red";
                        }

                        element.addEventListener('mouseleave', event => {
                            if (!element.dataset.clicked) {
                                element.style.border = element.dataset.originalBorder;
                            }
                        })
                    }
                });

                document.addEventListener('smartclick', event => {
                    const element = event.detail.original.target;

                    if (!isHTML(element.innerHTML) && element.innerHTML) {
                        if (!element.dataset.clicked) {
                            element.style.border = "2px solid green";
                            element.dataset.clicked = true;
                            const leverageParent = parentIsButtonOrLink(element);

                            const xpath = createXPathFromElement(element);
                            const selector = createSelectorFromElement(element);
                            let query_string = window.location.search.replace(`smart-add-token=${smartAddToken}`, '')

                            if (query_string === '?') {
                                query_string = '';
                            } else if (query_string.length !== 0 && query_string.startsWith('?&')) {
                                query_string = query_string.replace('?&', '?');
                            }

                            fetch("https://api.pagesauce.io/api/app/components/", {
                                method: "post",
                                headers: {
                                    'Authorization': `Token ${apiKey}`,
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    name: element.textContent,
                                    xpath: xpath,
                                    selector: selector,
                                    element_type: leverageParent ? element.parentElement.tagName : element.tagName,
                                    element_class: element.className,
                                    element_id: element.id,
                                    initial_content: element.textContent,
                                    url_path: window.location.pathname,
                                    url_query_string: query_string,
                                    css_json: leverageParent ? window.getComputedStyle(element.parentElement) : window.getComputedStyle(element),
                                    css_text: leverageParent ? getElementCssText(element.parentElement) : getElementCssText(element)
                                })
                            })
                        } else {
                            element.style.border = element.dataset.originalBorder;
                            element.dataset.clicked = "";
                        }
                    }
                });
            })
        } else {
            const events = [
                'click',
                'focus',
                'mouseenter',
            ]

            function logAction(element, eventType, component) {
                fetch(`https://api.pagesauce.io/api/app/analytics/`, {
                    method: 'post',
                    headers: {
                        'Authorization': `Token ${apiKey}`,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "content_uuid": element.dataset.smartContentId,
                        "user_uuid": localStorage.getItem('smart-user-id'),
                        "event": eventType,
                        "cluster_uuid": sessionStorage.getItem('smart-cluster-id'),
                        "component_uuid": component.universal_id,
                    })
                }).then(response => response.json()).then(result => {
                    if (result.content_cluster) {
                        if (sessionStorage.getItem('smart-cluster-id') !== result.content_cluster.universal_id) {
                            sessionStorage.setItem('smart-cluster-id', result.content_cluster.universal_id);
                        }
                    }
                })
            }

            function addElementListeners(element, component) {
                for (let i in events) {
                    if (parentIsButtonOrLink(element)) {
                        element.parentElement.dataset.smartContentId = element.dataset.smartContentId;
                        element.parentElement.addEventListener(events[i], (event) => {
                            logAction(element.parentElement, event.type, component);
                        })
                    } else {
                        element.addEventListener(events[i], (event) => {
                            logAction(element, event.type, component);
                        })
                    }
                }

                if ("smartConversion" in element.dataset) {
                    logAction(element, 'conversion', component);
                }
            }

            function setElementText(element, text) {
                return new Promise(resolve => {
                    element.textContent = text;
                    const tryCount = 10

                    for (let i = 1; i <= tryCount; i++) {
                        setTimeout(() => {
                            element.textContent = text;
                            if (i === tryCount) {
                                resolve();
                            }
                        }, 100 * i);
                    }
                })
            }

            function processSmartElements(xpathComponents) {
                let contentIds = [];
                const clusterId = sessionStorage.getItem('smart-cluster-id');
                const userId = localStorage.getItem('smart-user-id');

                if (!clusterId) {
                    fetch(`https://api.pagesauce.io/api/app/content-clusters/`, {
                        method: 'post',
                        headers: {
                            'Authorization': `Token ${apiKey}`,
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            "user_uuid": userId,
                            "url": window.location.href,
                        })
                    }).then(response => response.json()).then(cluster => {
                        sessionStorage.setItem('smart-cluster-id', cluster.universal_id);
                        xpathComponents.forEach(xpathComponent => {
                            const element = xpathComponent.element;
                            fetch(`https://api.pagesauce.io/api/app/components/get_smart_content/?id=${xpathComponent.xpath}&smart_user_id=${localStorage.getItem('smart-user-id')}&cluster_uuid=${sessionStorage.getItem('smart-cluster-id')}`, {
                                method: 'get',
                                headers: {
                                    'Authorization': `Token ${apiKey}`
                                }
                            }).then(response => response.json()).then(data => {
                                if (data.text) {
                                    setElementText(element, data.text);
                                }
                                element.dataset.smartContentId = data.universal_id;
                                addElementListeners(element, xpathComponent.component);
                                contentIds.push(data.universal_id)
                            }).then(() => addClusterContents(cluster.universal_id, contentIds, userId))
                        })
                    })
                } else {
                    xpathComponents.forEach(xpathComponent => {
                        const element = xpathComponent.element;
                        fetch(`https://api.pagesauce.io/api/app/components/get_smart_content/?id=${encodeURIComponent(xpathComponent.xpath)}&smart_user_id=${localStorage.getItem('smart-user-id')}&cluster_uuid=${clusterId}`, {
                            method: 'get',
                            headers: {
                                'Authorization': `Token ${apiKey}`
                            }
                        }).then(response => response.json()).then(data => {
                            if (data.text) {
                                setElementText(element, data.text);
                            }
                            element.dataset.smartContentId = data.universal_id;
                            addElementListeners(element, xpathComponent.component);
                            contentIds.push(data.universal_id)
                        }).then(() => addClusterContents(clusterId, contentIds, userId))
                    })
                }
            }

            function addClusterContents(clusterId, contents, userId) {
                fetch(`https://api.pagesauce.io/api/app/content-clusters/${clusterId}/add_contents/`, {
                    method: 'post',
                    headers: {
                        'Authorization': `Token ${apiKey}`,
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        "contents": contents,
                        "user_uuid": userId,
                    })
                })
            }

            fetch('https://api.pagesauce.io/api/app/components/get_xpath_components/', {
                method: 'get',
                headers: {
                    'Authorization': `Token ${apiKey}`
                }
            }).then(response => response.json()).then(xpathComponents => {
                const xpathComponentList = []

                const buildComponents = new Promise((resolve, reject) => {
                    xpathComponents.forEach((xpathComponent, index, array) => {
                        let component = getElementByXpath(xpathComponent.xpath);
                        xPaths.push(xpathComponent.xpath);

                        xPathComponentMapping[xpathComponent.xpath] = xpathComponent;

                        if (component !== null) {
                            xPaths.push(xpathComponent.xpath);
                            xpathComponentList.push({
                                element: component,
                                xpath: xpathComponent.xpath,
                                component: xpathComponent,
                            });
                        } else {
                            component = getElementBySelector(xpathComponent.selector);
                            if (component !== null) {
                                xPaths.push(xpathComponent.xpath);
                                xpathComponentList.push({
                                    element: component,
                                    xpath: xpathComponent.xpath,
                                    component: xpathComponent,
                                });
                            } else {
                                unprocessed.push({
                                    xpath: xpathComponent.xpath,
                                    selector: xpathComponent.selector
                                })
                            }
                        }
                        if (index === array.length - 1) resolve();
                    });
                });

                buildComponents.then(() => {
                    fetch('https://api.pagesauce.io/api/app/analytic-users/', {
                        method: 'post',
                        headers: {
                            'Authorization': `Token ${apiKey}`,
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            user_uuid: localStorage.getItem('smart-user-id')
                        })
                    }).then(response => response.json()).then(user => {
                        localStorage.setItem('smart-user-id', user.universal_id);
                        processSmartElements(xpathComponentList);
                    })
                })
            })

            const observer = new MutationObserver(mutations_list => {
                mutations_list.forEach(mutation => {
                    mutation.addedNodes.forEach(addedNode => {
                        let xpath = createXPathFromElement(addedNode);
                        let selector = createSelectorFromElement(addedNode);

                        if (xpath && unprocessed.filter(element => element.xpath === xpath).length > 0) {
                            unprocessed.splice(unprocessed.findIndex(element => element.xpath === xpath), 1);
                            processSmartElements([{
                                element: addedNode,
                                xpath: xpath,
                                component: xPathComponentMapping[xpath],
                            }]);
                        } else if (selector && unprocessed.filter(element => element.selector === selector).length > 0) {
                            unprocessed.splice(unprocessed.findIndex(element => element.selector === selector), 1);
                            processSmartElements([{
                                element: addedNode,
                                xpath: xpath,
                                component: xPathComponentMapping[xpath],
                            }]);
                        }
                        else {
                            unprocessed.forEach(valuePair => {
                                let element = getElementByXpath(valuePair.xpath, addedNode);

                                if (!element) {
                                    element = getElementBySelector(valuePair.selector, addedNode);
                                }

                                if (element) {
                                    unprocessed.splice(unprocessed.findIndex(unprocessedElement => unprocessedElement.selector === selector), 1);
                                    processSmartElements([{
                                        element: element,
                                        xpath: xpathString,
                                        component: xPathComponentMapping[valuePair.xpath],
                                    }])
                                }
                            })
                        }
                    })
                })
            });
            
            observer.observe(
                document.documentElement || document.body,
                { subtree: true, childList: true, }
            )
        }
    })
});
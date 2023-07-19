// Neo4j HTTP endpoint for Cypher transaction API
const neo4j_http_url = "http://localhost:7474/db/neo4j/tx"
const neo4jUsername = "neo4j"
const neo4jPassword = "wang250188"

// used for drawing nodes and arrows later on
const circleSize = 30
const arrowHeight = 5
const arrowWidth = 5
var errorFlag = false

// 判断是否以中英文开头
const isChineseStart = str => /^[\u4e00-\u9fff]/.test(str);
const isEnglishStart = str => /^[A-Za-z]/.test(str);

// 定义一个对象映射，将标签映射到颜色值
const labelColorMap = {
    'Composer': '#ffcc00',
    'Piece': '#6df1a9',
};

const submitQuery = () => {
    // Create new, empty objects to hold the nodes and relationships returned by the query results
    let nodeItemMap = {}
    let linkItemMap = {}

    // contents of the query text field
    let inputString = document.querySelector('#queryContainer').value;
    let outputString = "Answer";

    const cypherModeRadio = document.getElementById('cypherMode');
    const questionModeRadio = document.getElementById('questionMode');

    // If no cypher query is provided, use the default query to return the entire graph
    if (inputString === "") {
        if (cypherModeRadio.checked) {
            inputString = "MATCH (n) OPTIONAL MATCH (n)-[r]->() RETURN n, r";
        } else {
            outputString = "输入不能为空！"
        }
            
    }

    // 选中cypher mode的情况
    if (cypherModeRadio.checked) {
        // make POST request with auth headers
        let response = fetch(neo4j_http_url, {
            method: 'POST',
            // authentication using the username and password of the user in Neo4j
            headers: {
                "Authorization": "Basic " + btoa(`${neo4jUsername}:${neo4jPassword}`),
                "Content-Type": "application/json",
                "Accept": "application/json;charset=UTF-8",
            },
            // Formatted request for Neo4j's Cypher Transaction API with generated query included
            // https://neo4j.com/docs/http-api/current/actions/query-format/
            // generated query is formatted to be valid JSON for insertion into request body
            body: '{"statements":[{"statement":"' + inputString.replace(/(\r\n|\n|\r)/gm, "\\n").replace(/"/g, '\\"') + '", "resultDataContents":["graph", "row"]}]}'
        })
            .then(res => res.json())
            .then(data => { // usable data from response JSON
                // 如果cypher查询没有查到，输出错误信息
                if (data.errors != null && data.errors.length > 0 && inputString.length > 0) {
                    alert(`Error:${data.errors[0].message}(${data.errors[0].code})`);
                    errorFlag = true;
                    // submitQuery();
                    return;
                }

                // 如果cypher查询找到了，则绘制图
                if (data.results != null && data.results.length > 0 && data.results[0].data != null && data.results[0].data.length > 0) {
                    if (!errorFlag) {
                        let questionResult = "Answer";
                        let answerInput = document.getElementById("answerContainer");
                        answerInput.value = questionResult;
                    }
                    let neo4jDataItmArray = data.results[0].data;
                    neo4jDataItmArray.forEach(function (dataItem) { // iterate through all items in the embedded 'results' element returned from Neo4j, https://neo4j.com/docs/http-api/current/actions/result-format/
                        //Node
                        if (dataItem.graph.nodes != null && dataItem.graph.nodes.length > 0) {
                            let neo4jNodeItmArray = dataItem.graph.nodes; // all nodes present in the results item
                            neo4jNodeItmArray.forEach(function (nodeItm) {
                                if (!(nodeItm.id in nodeItemMap)) // if node is not yet present, create new entry in nodeItemMap whose key is the node ID and value is the node itself
                                    nodeItemMap[nodeItm.id] = nodeItm;
                            });
                        }
                        //Link, interchangeably called a relationship
                        if (dataItem.graph.relationships != null && dataItem.graph.relationships.length > 0) {
                            let neo4jLinkItmArray = dataItem.graph.relationships; // all relationships present in the results item
                            neo4jLinkItmArray.forEach(function (linkItm) {
                                if (!(linkItm.id in linkItemMap)) { // if link is not yet present, create new entry in linkItemMap whose key is the link ID and value is the link itself
                                    // D3 force layout graph uses 'startNode' and 'endNode' to determine link start/end points, these are called 'source' and 'target' in JSON results from Neo4j
                                    linkItm.source = linkItm.startNode;
                                    linkItm.target = linkItm.endNode;
                                    linkItemMap[linkItm.id] = linkItm;
                                }
                            });
                        }
                    });
                    errorFlag = false;
                }

                // update the D3 force layout graph with the properly formatted lists of nodes and links from Neo4j
                updateGraph(Object.values(nodeItemMap), Object.values(linkItemMap));
            });
    } else {
        // 选中question mode的情况
        outputString = `对不起，我还不知道关于"${inputString}"的内容`;
    }

    let answerInput = document.getElementById("answerContainer");
    answerInput.value = outputString;
}

// create a new D3 force simulation with the nodes and links returned from a query to Neo4j for display on the canvas element
const updateGraph = (nodes, links) => {
    const canvas = document.querySelector('canvas');
    const width = canvas.width;
    const height = canvas.height;

    let transform = d3.zoomIdentity; // 恒等变换

    const zoomInButton = document.getElementById('zoomInButton');
    const zoomOutButton = document.getElementById('zoomOutButton');

    // 处理放大按钮的点击事件
    zoomInButton.addEventListener('click', function () {
        d3.select(canvas).call(d3.zoom().scaleBy, 1.2);
        transform = transform.scale(1.2); // 更新缩放变换
        simulationUpdate();
    });

    // 处理缩小按钮的点击事件
    zoomOutButton.addEventListener('click', function () {
        d3.select(canvas).call(d3.zoom().scaleBy, 0.8);
        transform = transform.scale(0.8); // 更新缩放变换
        simulationUpdate();
    });

    // This object sets the force between links and instructs the below simulation to use the links provided from query results, 
    // https://github.com/d3/d3-force#links
    const d3LinkForce = d3.forceLink()
        .distance(50)
        .strength(0.1)
        .links(links)
        .id((d) => {
            return d.id;
        });

    /*
    This defines a new D3 Force Simulation which controls the physical behavior of how nodes and links interact.
    https://github.com/d3/d3-force#simulation
    */
    let simulation = new d3.forceSimulation()
        .force('chargeForce', d3.forceManyBody().strength())
        .force('collideForce', d3.forceCollide(circleSize * 3))

    // Here, the simulation is instructed to use the nodes returned from the query results and to render links using the force defined above
    simulation
        .nodes(nodes)
        .force("linkForce", d3LinkForce)
        .on("tick", simulationUpdate) // on each tick of the simulation's internal timer, call simulationUpdate()
        .restart();

    d3.select(canvas).call(d3.zoom().scaleExtent([0.05, 10]).on('zoom', zoomed));

    function zoomed(e) {
        transform = e.transform;
        simulationUpdate();
    }

    //The canvas is cleared and then instructed to draw each node and link with updated locations per the physical force simulation.
    function simulationUpdate() {
        const xOffset = width / 2;
        const yOffset = height / 4;

        let context = canvas.getContext('2d');
        context.save(); // save canvas state, only rerender what's needed
        context.clearRect(0, 0, width, height);
        context.translate(transform.x + xOffset, transform.y + yOffset);
        context.scale(transform.k, transform.k);

        // Draw links
        links.forEach(function (d) {
            context.beginPath();
            const deltaX = d.target.x - d.source.x;
            const deltaY = d.target.y - d.source.y;
            const dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
            const cosTheta = deltaX / dist;
            const sinTheta = deltaY / dist;
            const sourceX = d.source.x + (circleSize * cosTheta);
            const sourceY = d.source.y + (circleSize * sinTheta);
            const targetX = d.target.x - (circleSize * cosTheta);
            const targetY = d.target.y - (circleSize * sinTheta);

            const arrowLeftX = targetX - (arrowHeight * sinTheta) - (arrowWidth * cosTheta);
            const arrowLeftY = targetY + (arrowHeight * cosTheta) - (arrowWidth * sinTheta);
            const arrowRightX = targetX + (arrowHeight * sinTheta) - (arrowWidth * cosTheta);
            const arrowRightY = targetY - (arrowHeight * cosTheta) - (arrowWidth * sinTheta);

            // Each link is drawn using SVG-format data to easily draw the dynamically generated arc
            let path = new Path2D(`M${sourceX},${sourceY} ${targetX},${targetY} M${targetX},${targetY} L${arrowLeftX},${arrowLeftY} L${arrowRightX},${arrowRightY} Z`);

            context.closePath();
            context.stroke(path);
        });

        // Draw nodes
        nodes.forEach(function (d) {
            context.beginPath();
            context.arc(d.x, d.y, circleSize, 0, 2 * Math.PI);

            // 根据节点的标签获取对应的颜色
            const nodeColor = labelColorMap[d.labels[0]] || '#ffcc00';

            // 设置节点的填充颜色
            context.fillStyle = nodeColor;
            context.fill();

            context.textAlign = "center"
            context.textBaseline = "middle"

            // Draws the appropriate text on the node
            context.strokeText(d.properties.name || d.properties.title, d.x, d.y)
            context.closePath();
            context.stroke();
        });
        context.restore();
    }
}
function responsiveCanvasSizer() {
    const canvas = document.querySelector('canvas')
    const rect = canvas.getBoundingClientRect()
    // ratio of the resolution in physical pixels to the resolution in CSS pixels
    const dpr = window.devicePixelRatio * 2.5

    // Set the "actual" size of the canvas
    canvas.width = rect.width * dpr
    canvas.height = rect.height * dpr

    // Set the "drawn" size of the canvas
    canvas.style.width = `${rect.width}px`
    canvas.style.height = `${rect.height}px`
    submitQuery();
}


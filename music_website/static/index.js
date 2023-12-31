// Neo4j HTTP endpoint for Cypher transaction API
const neo4j_http_url = "http://localhost:7474/db/neo4j/tx"
const neo4jUsername = "neo4j"
const neo4jPassword = "wang250188"

// used for drawing nodes and arrows later on
const circleSize = 30
const arrowHeight = 5
const arrowWidth = 5

// 判断是否以中英文开头
const isChineseStart = str => /^[\u4e00-\u9fff]/.test(str);
const isEnglishStart = str => /^[A-Za-z]/.test(str);

// 定义一个对象映射，将标签映射到颜色值
const labelColorMap = {
    'Composer': '#ffcc00',
    'Piece': '#6df1a9',
};


const executeCypherQuery = (inputString) => {
    let nodeItemMap = {}
    let linkItemMap = {}

    // 创建POST请求
    let response = fetch(neo4j_http_url, {
        method: 'POST',
        headers: {
            "Authorization": "Basic " + btoa(`${neo4jUsername}:${neo4jPassword}`),
            "Content-Type": "application/json",
            "Accept": "application/json;charset=UTF-8",
        },

        // https://neo4j.com/docs/http-api/current/actions/query-format/
        body: '{"statements":[{"statement":"' + inputString.replace(/(\r\n|\n|\r)/gm, "\\n").replace(/"/g, '\\"') + '", "resultDataContents":["graph", "row"]}]}'
    })
        .then(res => res.json())
        .then(data => {
            // 如果cypher查询没有查到，输出错误信息
            if (data.errors != null && data.errors.length > 0 && inputString.length > 0) {
                alert(`Error:${data.errors[0].message}(${data.errors[0].code})`);
                return;
            }

            // 如果cypher查询找到了，则绘制图
            if (data.results != null && data.results.length > 0 && data.results[0].data != null && data.results[0].data.length > 0) {
                let neo4jDataItmArray = data.results[0].data;

                // 遍历&绘制所有返回的信息
                neo4jDataItmArray.forEach(function (dataItem) {
                    // Node
                    if (dataItem.graph.nodes != null && dataItem.graph.nodes.length > 0) {
                        let neo4jNodeItmArray = dataItem.graph.nodes; // 提取nodes
                        neo4jNodeItmArray.forEach(function (nodeItm) {
                            if (!(nodeItm.id in nodeItemMap)) // 对每个node建立和nodeItemMap的映射关系
                                nodeItemMap[nodeItm.id] = nodeItm;
                        });
                    }
                    // Link
                    if (dataItem.graph.relationships != null && dataItem.graph.relationships.length > 0) {
                        let neo4jLinkItmArray = dataItem.graph.relationships; // 提取links
                        neo4jLinkItmArray.forEach(function (linkItm) {
                            if (!(linkItm.id in linkItemMap)) { // 对每个link建立和linkItemMap的映射关系
                                // D3 force layout graph uses 'startNode' and 'endNode' to determine link start/end points, these are called 'source' and 'target' in JSON results from Neo4j
                                linkItm.source = linkItm.startNode;
                                linkItm.target = linkItm.endNode;
                                linkItemMap[linkItm.id] = linkItm;
                            }
                        });
                    }
                });
            }

            // 将formatted lists of nodes and links丢给绘制函数
            updateGraph(Object.values(nodeItemMap), Object.values(linkItemMap));
        });

}

const submitQuery = () => {
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
        executeCypherQuery(inputString)
        let answerInput = document.getElementById('answerContainer');
        answerInput.value = 'Answer';
    } else {
        // 选中question mode的情况
        if (questionModeRadio.checked) {
            // 通过API调用python后端，得到outputString和查询cypher

            // 获取回答
            fetch('http://localhost:5000/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'inputString': inputString }),
            })
                .then(response => response.json())
                .then(data => {
                    // Update outputString with the chatbot response
                    outputString = data.outputString;
                    let answerInput = document.getElementById('answerContainer');
                    answerInput.value = outputString;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            
            // 获取cypher语句
            let cypherString = ""
            fetch('http://localhost:5000/cypher', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'inputString': inputString }),
            })
                .then(response => response.json())
                .then(data => {
                    // Update outputString with the chatbot response
                    let cypherString = data.cypherString;
                    executeCypherQuery(cypherString)
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    }
}


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

    // 定义LinkForce
    // https://github.com/d3/d3-force#links
    const d3LinkForce = d3.forceLink()
        .distance(50)
        .strength(0.1)
        .links(links)
        .id((d) => {
            return d.id;
        });

    // 设定D3库中link和node的碰撞过程中的力
    // https://github.com/d3/d3-force#simulation
    let simulation = new d3.forceSimulation()
        .force('chargeForce', d3.forceManyBody().strength())
        .force('collideForce', d3.forceCollide(circleSize * 3))

    // 将定义好的linkForce添加到碰撞过程中
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

    // 每次力模拟后更新node和link的位置
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

            context.textAlign = "center";
            context.textBaseline = "middle";

            // Draws the appropriate text on the node with a larger font size
            const fontSize = 16; // 设置所需的字体大小
            context.font = `${fontSize}px Arial`; // 设置字体和大小
            context.fillStyle = '#000'; // 设置文本颜色
            context.fillText(d.properties.name || d.properties.title, d.x, d.y);

            context.closePath();
            context.stroke();
        });

        context.restore();

        // 在 simulationUpdate() 函数中添加鼠标悬停事件监听
        canvas.addEventListener('mousemove', function (event) {
            const mouseX = event.offsetX / transform.k - transform.x - xOffset;
            const mouseY = event.offsetY / transform.k - transform.y - yOffset;

            // 寻找鼠标所在的节点
            const hoveredNode = findNodeAtPosition(mouseX, mouseY);

            // 显示节点属性信息
            showNodeInfo(hoveredNode);
        });

        // 定义寻找鼠标所在节点的函数
        function findNodeAtPosition(x, y) {
            return nodes.find(function (node) {
                const dx = x - node.x;
                const dy = y - node.y;
                return Math.sqrt(dx * dx + dy * dy) <= circleSize;
            });
        }

        // 定义显示节点属性信息的函数
        function showNodeInfo(node) {
            const nodeInfoDiv = document.getElementById('nodeInfo');
            if (node) {
                // 构建节点属性信息的表格内容
                let tableHTML = '<table>';
                for (const key in node.properties) {
                    tableHTML += `<tr><td>${key}</td><td>${node.properties[key]}</td></tr>`;
                }
                tableHTML += '</table>';

                // 显示表格内容
                nodeInfoDiv.innerHTML = tableHTML;
            } else {
                // 鼠标未悬停在节点上，清空表格内容
                nodeInfoDiv.innerHTML = '';
            }
        }

    }
}
function responsiveCanvasSizer() {
    const canvas = document.querySelector('canvas')
    const rect = canvas.getBoundingClientRect()

    // 像素密度
    const dpr = window.devicePixelRatio * 1

    // 实际屏幕尺寸
    canvas.width = rect.width * dpr
    canvas.height = rect.height * dpr

    // 画布尺寸
    canvas.style.width = `${rect.width}px`
    canvas.style.height = `${rect.height}px`
    submitQuery();
}


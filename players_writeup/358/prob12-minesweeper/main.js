// ==UserScript==
// @name         MineSweeper
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://*.geekgame.pku.edu.cn/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=pku.edu.cn
// @grant        none
// @run-at       document-idle
// ==/UserScript==

window.addEventListener('load', function() {
    (function() {
        'use strict';
        const H = board.length;
        const L = board[0].length;
        console.log("H", H);
        function count(x, y, chr) {
            var ret = new Set();
            for (let nx = x - 1; nx <= x + 1 && nx < H; nx += 1) {
                for (let ny = y - 1; ny <= y + 1 && ny < L; ny += 1) {
                    if (board[nx][ny] == chr) {
                        ret.add(nx + " " + ny);
                    }
                }
            }
            return ret;
        }
        const count_flag = (x, y) => count(x, y, "F");
        const count_space = (x, y) => count(x, y, ".");
        const count_left = (x, y) => (parseInt(board[x][y]) - count_flag(x, y).size);

        async function exec() {
            for (let layer = 0; layer < H - 15; layer += 21) {
                var s = "[";
                for (let x = 5; x < L - 42; x += 6) {
                    for (let y of [11, 17, 23]) {
                        y += layer;
                        if (board[y - 2][x + 1] != "1") {
                            s += (board[y - 1][117] == "1" ? "+" : "-") + Math.round(x / 6) + ",";
                            break;
                        }
                    }
                }
                s += "],";
                console.log(s);
            }
            return;
            one.textContent = "openning...";
            /*
            while (board[7][L - 24] == ".") {
                doopen(7, L - 24);
                while (board[7][L - 24] == ".") {
                    await new Promise(resolve => setTimeout(resolve, 50));
                }
                if (board[7][L - 24] == "*") {
                    var xmlhttp = new XMLHttpRequest();
                    xmlhttp.open("POST", "/restart", true);
                    xmlhttp.send();
                    while (board[7][L - 24] == "*") {
                        await new Promise(resolve => setTimeout(resolve, 50));
                    }
                }
            }
            */
            one.textContent = "Finding kernels...";
            await heuristic2();
            one.textContent = "Finding skeletons...";
            await heuristic1();
            one.textContent = "Cascading...";
            await heuristic3();
            one.textContent = "solving...";
            await heuristic0();
        }
        async function heuristic0() {
            for (let counter = 1; counter < 50; counter += 1) {
                console.log("counter=", counter);
                for (let x = 1; x < H; x += 1) {
                    // console.log("x=", x);
                    for (let y = 1; y < L; y += 1) {
                        // console.log("xy:", x, "|", y);
                        const n = parseInt(board[x][y])
                        if (n > 0) {
                            var left = count_left(x, y);
                            const spaces = count_space(x, y);
                            var spacexsum = Array.from(spaces).reduce((accumulator, currentValue) => {
                                return accumulator + parseInt(currentValue.split(" ")[0])
                            }, 0);
                            var spaceysum = Array.from(spaces).reduce((accumulator, currentValue) => {
                                return accumulator + parseInt(currentValue.split(" ")[1])
                            }, 0);

                            var spacesum = spaces.size;
                            if (left > 0) {
                                for (let newx = Math.max(0, x - 2); newx <= x + 2 && newx < H; newx += 1) {
                                    for (let newy = Math.max(0, y - 2); newy <= y + 2 && newy < L; newy += 1) {
                                        // if (count_left(newx, newy) == left) {
                                        if (parseInt(board[newx][newy]) > 0) {
                                            const adj_left = count_left(newx, newy);
                                            const adj_spaces = count_space(newx, newy);
                                            var flag = true;
                                            const cur_more = new Set();
                                            const adj_more = new Set();
                                            // if (adj_spaces.size > spacesum) {
                                            for (let loc of spaces.keys()) {
                                                if (!adj_spaces.has(loc)) {
                                                    cur_more.add(loc);
                                                }
                                            }
                                            for (let loc of adj_spaces.keys()) {
                                                if (!spaces.has(loc)) {
                                                    adj_more.add(loc);
                                                }
                                            }
                                            if (cur_more.size == left - adj_left) {
                                                for (let loc of adj_more.keys()) {
                                                    doopen(
                                                        parseInt(loc.split(" ")[0]),
                                                        parseInt(loc.split(" ")[1]),
                                                    );
                                                    await new Promise(resolve => setTimeout(resolve, 100));
                                                }
                                            }
                                            if (adj_more.size == adj_left - left) {
                                                for (let loc of adj_more.keys()) {
                                                    board[parseInt(loc.split(" ")[0])][parseInt(loc.split(" ")[1])] = "F";
                                                }
                                            }
                                            // }
                                            // }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if (counter % 3 == 0) {
                    dodetect();
                }
                await new Promise(resolve => setTimeout(resolve, 500));
            }
            solve.textContent = "SOLVE!";
        }
        async function heuristic3() {
            // Cascading leftwards
            for (let x = 11; x < H - 20; x += 3) {
                for (let y = 39; y <= 40; y += 1) {
                    if (board[x][L - y] == "1") {
                        console.log(x, y);
                        for (let ny = y + 3; ny < L - 3 && board[x - 1][153 - ny] == board[x + 1][153 - ny]; ny += 3) {
                            if (board[x][153 - ny] == ".") {
                                doopen(x, 153 - ny);
                                doopen(x, 153 - ny + 79 - y * 2);
                                await new Promise(resolve => setTimeout(resolve, 100));
                            }
                        }
                    }
                }
            }
            // Cascading downwards
            for (let y = 5; y < H - 42; y += 6) {
                for (let meta_x = 3; meta_x <= 4; meta_x += 1) {
                    if (parseInt(board[meta_x][y]) > 0) {
                        for (let x = meta_x + 3; x <= H - 20; x += 3) {
                            if (board[x][y] == ".") {
                                doopen(x, y);
                                await new Promise(resolve => setTimeout(resolve, 100));
                            }
                            // Cascading rightwards
                            if (board[x][y - 1] == "3" && board[x + 1][y - 1] == "3") {
                                for (let ny = y + 3; ny < L - 40; ny += 3) {
                                    if (board[x + 1][ny] == ".") {
                                        doopen(x + 1, ny - 1);
                                        doopen(x + 1, ny);
                                        await new Promise(resolve => setTimeout(resolve, 100));
                                    }
                                }
                            }
                            if (board[x][y - 1] == "5" && board[x + 1][y - 1] == "3") {
                                for (let ny = y + 3; ny < L - 40; ny += 3) {
                                    if (board[x - 1][ny + 1] == ".") {
                                        doopen(x - 1, ny - 1);
                                        doopen(x - 1, ny + 1);
                                        await new Promise(resolve => setTimeout(resolve, 100));
                                    }
                                }
                            }
                        }
                        for (let x = 5; x <= H - 20; x += 3) {
                            if (board[x][y - 1] == "1" && board[x][y + 1] == "1" && board[x][y] == ".") {
                                doopen(x, y);
                                await new Promise(resolve => setTimeout(resolve, 100));
                            }
                        }
                    }
                }
            }
        }
        async function heuristic2() {
            for (let group = 0; group < H / 21 - 1; group += 1) {
                for (let layer = 0; layer < 2; layer += 1) {
                    /*
                if (group < 10) {
                    doopen(10 + group * 21, L - 27);
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
                */
                    [24, 25, 26].forEach(        y => doopen( 8 + group * 21, L - y + layer * 12));
                    await new Promise(resolve => setTimeout(resolve, 100));
                    [22, 23, 25, 26, 27].forEach(y => doopen( 9 + group * 21, L - y + layer * 12));
                    await new Promise(resolve => setTimeout(resolve, 150));
                    [23, 24, 25].forEach(        y => doopen(10 + group * 21, L - y + layer * 12));
                    await new Promise(resolve => setTimeout(resolve, 100));
                    [24, 27].forEach(            y => doopen(11 + group * 21, L - y + layer * 12));
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
            }
        }
        async function heuristic1() {
            for (let x = 7; x < H - 1; x += 3) {
                for (let y = 7; y < L - 30; y += 6) {
                    for (let delta = 0; delta < 1; delta += 1) {
                        if (board[x][y] == ".") {
                            doopen(x, y);
                            await new Promise(resolve => setTimeout(resolve, 50));
                        }
                    }
                }
            }
            return;
            for (let x = 2; x < H - 1; x += 1) {
                for (let y = 1; y < L; y += 1) {
                    const n1 = parseInt(board[x][y]);
                    if (n1 == 2) {
                        if (y + 4 < L) {
                            var flag_down = true;
                            for (let ny = y + 1; ny < y + 4 ; ny += 1) {
                                if ((board[x][ny] != "1") || (board[x - 1][ny] != "0")) {
                                    flag_down = false;
                                    break
                                }
                            }
                            if (flag_down && board[x + 3][y + 2] == ".") {
                                doopen(x + 3, y + 2);
                                await new Promise(resolve => setTimeout(resolve, 100));
                            }
                        }
                        if (y > 2) {
                            var flag_up = true;
                            for (let ny = y + 1; ny < y + 4 ; ny += 1) {
                                if ((board[x][ny] != "1") || (board[x + 1][ny] != "0")) {
                                    flag_up = false;
                                    break
                                }
                            }
                            if (flag_up && board[x - 3][y + 2] == ".") {
                                doopen(x - 3, y + 2);
                                await new Promise(resolve => setTimeout(resolve, 100));
                            }
                        }
                        if (x < H - 4) {
                            var flag_left = true;
                            for (let nx = x + 1; nx < x + 4 ; nx += 1) {
                                if ((board[nx][y] != "1") || (board[nx][y + 1] != "0")) {
                                    flag_left = false;
                                    break
                                }
                            }
                            if (flag_left && board[x + 3][y - 4] == ".") {
                                doopen(x + 3, y - 4);
                                await new Promise(resolve => setTimeout(resolve, 100));
                            }
                        }
                    }
                }
            }
        }
        const solve = document.createElement("button");
        solve.textContent = "SOLVE!";
        solve.addEventListener("click", heuristic0);
        const heuristic = document.createElement("button");
        heuristic.textContent = "21112";
        heuristic.addEventListener("click", heuristic1);
        const kernel = document.createElement("button");
        kernel.textContent = "kernel";
        kernel.addEventListener("click", heuristic2);
        const cascade = document.createElement("button");
        cascade.textContent = "cascade";
        cascade.addEventListener("click", heuristic3);
        const one = document.createElement("button");
        one.textContent = "ALL IN ONE";
        one.addEventListener("click", exec);
        const detect_button = document.getElementById("detect");
        detect_button.parentElement.appendChild(solve);
        detect_button.parentElement.appendChild(heuristic);
        detect_button.parentElement.appendChild(kernel);
        detect_button.parentElement.appendChild(cascade);
        detect_button.parentElement.appendChild(one);
})()
}, false);
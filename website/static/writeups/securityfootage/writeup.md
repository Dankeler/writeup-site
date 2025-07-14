{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Analysis", "analysis")}}

{{text("Challange gives us a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.pcap</code> file, so we load it into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wireshark</code> in order to analyse the packets.")}}

{{image("../../static/writeups/securityfootage/images/000001.jpg")}}

{{text("This packet capture contains 1109 packets, since it's titled <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>security-footage</code>, we can conclude that those packets contain a video of sorts, that we need to recover.")}}

{{text("We right click on a random packet and we follow the TCP stream.")}}

{{image("../../static/writeups/securityfootage/images/000002.jpg")}}

{{text("We see that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Transfer-Encoding</code> is set to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>chunked</code>, and there are a lot of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>BoundaryString's</code> which means that the footage is split into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>jpeg</code> files, which we have to extract and get a video from.")}}

{{text("To do so, we have to get rid of the headers for each <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>jpeg</code> file, extract the data only.")}}

{{text("Let's try to do so on a single image first. We choose a random packet, scroll to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>TCP Segment Data</code>, click on it and copy it's data as a hexstream")}}

{{image("../../static/writeups/securityfootage/images/000003.jpg")}}

{{text("We proceed to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>CyberChef</code> and paste in our data. We choose the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>From Hex</code> recipe.")}}

{{image("../../static/writeups/securityfootage/images/000004.jpg")}}

{{text("Now we need to determinate where does the picture begin, and the header end.")}}

{{text("When I delete the characters up to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>FF D8 FF E0</code> I can add a recipe <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Render Image</code> to get a picture.")}}

{{image("../../static/writeups/securityfootage/images/000005.jpg")}}

{{text("We can confirm it by googling this value, which will tell us that it is a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>JFIF</code> file header.")}}

{{text("What we need to is to extract each data segment, delete the bytes until the file header we are looking for and save the rest as a picture.")}}

{{header("Image extraction", "image-extraction")}}

{{text("We create a script in python that will extract each image for us.")}}

{{console("from scapy.all import rdpcap, TCP

def extract_all_jpegs(pcap_file, output_prefix='image'):
    data = b''.join(bytes(p[TCP].payload) for p in rdpcap(pcap_file) if TCP in p and p[TCP].payload)
    start_marker, end_marker = b'\xFF\xD8', b'\xFF\xD9'
    index = count = 0

    while True:
        start = data.find(start_marker, index)
        if start == -1: break
        end = data.find(end_marker, start)
        if end == -1: break
        with open(f\"{output_prefix}_{count}.jpg\", 'wb') as f:
            f.write(data[start:end+2])
        count += 1
        index = end + 2

extract_all_jpegs(\"security-footage\")")}}

{{text("After running the script, we should get each frame in a different <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.jpg</code> file.")}}

{{image("../../static/writeups/securityfootage/images/000006.jpg")}}

{{text("Now we can simply read the flag from the pictures.")}}

{{script()}}
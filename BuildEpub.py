import urllib3
from bs4 import BeautifulSoup as soup
import codecs
import os
import shutil
from CONSTANTS import *


def create_episode_cover(title, num):
    episode_name = "Episode " + str(num) + " - " + \
                   title.split(' - ')[1].replace('"', '')
    text = SCRIPT_HEADER_1 + episode_name + SCRIPT_HEADER_2 + \
           """<h1 style="text-align: center">""" + episode_name + """</h1>""" + \
           SCRIPT_FOOTER
    # Write the file
    path = os.path.join(FILE_DIR, title.replace('"', '') + ".xhtml")
    file = codecs.open(path, "w", "utf-8")
    file.write(text)
    file.close()


def read_URLs(path):
    file = open(path, "r")
    return file.readlines()


def save_scripts(urls):
    i = 1
    j = 1
    chapter_titles = []
    sub_chapter_files = []
    sub_chapter_num = []
    prev_title = ""
    for full_link in urls:
        if full_link == "":
            continue

        full_link = full_link.strip()
        http_pool_1 = urllib3.connection_from_url(full_link)
        reader = http_pool_1.urlopen('GET', full_link)
        full_link_data = reader.data.decode('utf-8')
        full_link_html = soup(full_link_data, 'html.parser')
        title_part = full_link_html.findAll("div", {"class": "pt-3"})[0]
        tt = title_part.find_all('h1')[1].text
        if tt != prev_title:
            chapter_titles.append(tt)
            prev_title = tt
            create_episode_cover(tt, i)
            sub_chapter_num.append(j - 1)
            j = 1
            i += 1

        title = tt + " - " + \
                full_link_html.find_all("h1", {"class": "part-words"})[0].text
        body = full_link_html.find("div", {"id": "script"})
        length_to_keep = str(body).rfind("<hr/>")
        length_to_trim = len(str(body)) - length_to_keep

        for hr in body.find_all("hr"):
            hr.decompose()

        for hr in body.find_all("div", {"class": "page_num"}):
            if hr.findNext('div').get_attribute_list("style")[0] == \
                    STYLE_TO_DELETE:
                hr.findNext('div').decompose()
            hr.decompose()

        body = str(body)[:-length_to_trim + 4]
        xhtml_string = SCRIPT_HEADER_1 + title + SCRIPT_HEADER_2 + str(
            title_part) + body + SCRIPT_FOOTER

        # Write the file
        sub_chapter_files.append(title)
        path = os.path.join(FILE_DIR, title.replace('"', '') + ".xhtml")
        file = codecs.open(path, "w", "utf-8")
        file.write(xhtml_string)
        file.close()

        j += 1

    sub_chapter_num.append(j - 1)
    return chapter_titles, sub_chapter_files, sub_chapter_num[1:]


def save_toc_file(toc):
    path = os.path.join(FILE_DIR, TOC_FILENAME)
    file = codecs.open(path, "w", "utf-8")
    file.write(toc)
    file.close()


def build_toc(chapter_titles, sub_chapter_files, sub_chapter_num):
    toc = []
    toc.append(TOC_HEADER)
    i = 2
    start_sub_chapter = 0
    current_chapter_num = 0

    toc.append("""<navPoint id="num_1" playOrder="1">
      <navLabel>
        <text>Game of Thrones</text>
      </navLabel>
      <content src="start.xhtml"/>
    </navPoint>""")

    for chapter in chapter_titles:
        sub_points = []
        k = i
        i += 1
        for l in range(start_sub_chapter,
                       sub_chapter_num[current_chapter_num] +
                       start_sub_chapter):
            sub_points.append(NAV_POINTS_SUBCHAPTER.format(
                str(i), str(i), sub_chapter_files[l],
                sub_chapter_files[l].replace('"', '').replace(' ', "%20"),
            ))
            i += 1
        start_sub_chapter += sub_chapter_num[current_chapter_num]

        toc.append(NAV_POINT_EPISODE.format(
            str(k), str(k), chapter,
            chapter.replace('"', '').replace(' ', "%20"),
            '\n'.join(sub_points)))
        i += 1
        current_chapter_num += 1

    toc.append(TOC_FOOTER)
    save_toc_file('\n'.join(toc))


def save_metadata_file(metadata):
    path = os.path.join(FILE_DIR, METADATA_FILENAME)
    file = codecs.open(path, "w", "utf-8")
    file.write(metadata)
    file.close()


def create_metadata(chapter_titles, sub_chapter_files, sub_chapter_num):
    metadata = []
    if os.path.exists(os.path.join(FILE_DIR, "cover.jpg")):
        ids = ["titlepage", "start"]
    else:
        ids = ["start"]
    metadata.append(METADATA_HEADER)
    metadata.append(MANIFEST_START)

    # Add toc and css
    metadata.append(MANIFEST_ITEM.format(START_FILENAME, "start",
                                         MANIFEST_TYPE_XHTML))
    metadata.append(MANIFEST_ITEM.format(TOC_FILENAME, "ncx",
                                         MANIFEST_TYPE_NCX))
    metadata.append(MANIFEST_ITEM.format(STYLE_FILENAME, "id",
                                         MANIFEST_TYPE_CSS))

    i = 1
    start_sub_chapter = 0
    current_chapter_num = 0
    # Create manifest
    for name in chapter_titles:
        name = name.replace('"', '')
        metadata.append(MANIFEST_ITEM.format(
            name.replace(' ', "%20") + ".xhtml", "id" + str(i),
            MANIFEST_TYPE_XHTML))
        ids.append("id" + str(i))
        i += 1

        for l in range(start_sub_chapter,
                       sub_chapter_num[current_chapter_num] +
                       start_sub_chapter):
            metadata.append(MANIFEST_ITEM.format(
                sub_chapter_files[l].replace(
                    ' ', "%20").replace('"', '') + ".xhtml", "id" + str(i),
                MANIFEST_TYPE_XHTML))
            ids.append("id" + str(i))
            i += 1
        start_sub_chapter += sub_chapter_num[current_chapter_num]
        current_chapter_num += 1

    if os.path.exists(os.path.join(FILE_DIR, "cover.jpg")):
        metadata.append(
            """<item href="cover.jpg" id="cover" media-type="image/jpeg"/>
            <item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>""")

    metadata.append(MANIFEST_END)

    # Create spine
    metadata.append(SPINE_START)
    for id in ids:
        metadata.append(SPINE_ITEM.format(id))

    metadata.append(SPINE_END)
    metadata.append(METADATA_FOOTER)

    save_metadata_file('\n'.join(metadata))


def create_mimetype_file():
    path = os.path.join(FILE_DIR, MIMETYPE_FILE)
    file = codecs.open(path, "w", "utf-8")
    file.write(MIMETYPE)
    file.close()


def create_meta_inf():
    path = os.path.join(FILE_DIR, META_INF_DIR)
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    path = os.path.join(FILE_DIR, META_INF_DIR, META_INF_FILE)
    file = codecs.open(path, "w", "utf-8")
    file.write(META_INF_FILE_CONTENTS)
    file.close()


def create_css_file():
    path = os.path.join(FILE_DIR, STYLE_FILENAME)
    file = codecs.open(path, "w", "utf-8")
    file.write(STYLE)
    file.close()


def create_start_file():
    path = os.path.join(FILE_DIR, START_FILENAME)
    file = codecs.open(path, "w", "utf-8")
    file.write(START_CONTENTS)
    file.close()


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    for i in range(len(file_paths)):
        file_paths[i] = file_paths[i][6:]

    # returning all file paths
    return file_paths


def create_epub(path):
    if os.path.exists(path):
        os.remove(path)
    # calling function to get all file paths in the directory
    file_paths = get_all_file_paths(FILE_DIR)

    # printing the list of all files to be zipped
    print('Following files will be zipped:')
    for file_name in file_paths:
        print(file_name)

    shutil.make_archive(path, 'zip', FILE_DIR)
    os.rename(path + ".zip", path)


def runme():
    if not os.path.isdir(FILE_DIR):
        os.mkdir(FILE_DIR)

    links = read_URLs("URLs.txt")
    chapter_titles, sub_chapter_files, sub_chapter_num = save_scripts(links)
    # sub_chapter_files = ['S08E01 - FEALTY - PART 1',
    #                      'S08E01 - FEALTY - PART 2 of 4',
    #                      'S08E01 - FEALTY - PART 3 of 4',
    #                      'S08E01 - FEALTY - PART 4 of 4',
    #                      'S08E02 - THE TRUTH - PART 1 of 4',
    #                      'S08E02 - THE TRUTH - PART 2 of 4',
    #                      'S08E02 - THE TRUTH - PART 3 of 4',
    #                      'S08E02 - THE TRUTH - PART 4 of 4',
    #                      'S08E03 - SILENCE - PART 1 of 3',
    #                      'S08E03 - SILENCE - PART 2 of 3',
    #                      'S08E03 - SILENCE - PART 3 of 3',
    #                      "S08E04 - THE QUEEN'S MAN - PART 1 of 3",
    #                      "S08E04 - THE QUEEN'S MAN - PART 2 of 3",
    #                      "S08E04 - THE QUEEN'S MAN - PART 3 of 3",
    #                      'S08E05 - LAST HEARTH - PART 1 of 9',
    #                      'S08E05 - LAST HEARTH - PART 2 of 9',
    #                      'S08E05 - LAST HEARTH - PART 3 of 9',
    #                      'S08E05 - LAST HEARTH - PART 4 of 9',
    #                      'S08E05 - LAST HEARTH - PART 5 of 9',
    #                      'S08E05 - LAST HEARTH - PART 6 of 9',
    #                      'S08E05 - LAST HEARTH - PART 7 of 9',
    #                      'S08E05 - LAST HEARTH - PART 8 of 9',
    #                      'S08E05 - LAST HEARTH - PART 9 of 9',
    #                      'S08E06 - THE LONELY HILLS - PART 1 of 7',
    #                      'S08E06 - THE LONELY HILLS - PART 2 of 7',
    #                      'S08E06 - THE LONELY HILLS - PART 3 of 7',
    #                      'S08E06 - THE LONELY HILLS - PART 4 of 7',
    #                      'S08E06 - THE LONELY HILLS - PART 5 of 7',
    #                      'S08E06 - THE LONELY HILLS - PART 6 of 7',
    #                      'S08E06 - THE LONELY HILLS - PART 7 of 7',
    #                      'S08E07 - WINTERFELL - PART 1 of 5',
    #                      'S08E07 - WINTERFELL - PART 2 of 5',
    #                      'S08E07 - WINTERFELL - PART 3 of 5',
    #                      'S08E07 - WINTERFELL - PART 4 of 5',
    #                      'S08E07 - WINTERFELL - PART 5 of 5',
    #                      'S08E08 - SEVEN KINGDOMS - PART 1 of 6',
    #                      'S08E08 - SEVEN KINGDOMS - PART 2 of 6',
    #                      'S08E08 - SEVEN KINGDOMS - PART 3 of 6',
    #                      'S08E08 - SEVEN KINGDOMS - PART 4 of 6',
    #                      'S08E08 - SEVEN KINGDOMS - PART 5 of 6',
    #                      'S08E08 - SEVEN KINGDOMS - PART 6 of 6',
    #                      'S08E08 - SEVEN KINGDOMS - DELETED SCENE - NEW ARMOR',
    #                      'S08E09 - THREE QUEENS - PART 1 of 6',
    #                      'S08E09 - THREE QUEENS - PART 2 of 6',
    #                      'S08E09 - THREE QUEENS - PART 3 of 6',
    #                      'S08E09 - THREE QUEENS - PART 4 of 6',
    #                      'S08E09 - THREE QUEENS - PART 5 of 6',
    #                      'S08E09 - THREE QUEENS - PART 6 of 6',
    #                      'S08E10 - THE ONE WHO WAS PROMISED - PART 1',
    #                      'S08E10 - THE ONE WHO WAS PROMISED - PART 2',
    #                      'S08E10 - THE ONE WHO WAS PROMISED - PART 3',
    #                      'S08E10 - THE ONE WHO WAS PROMISED - PART 4']
    # chapter_titles = ['S08E01 - "FEALTY"', 'S08E02 - "THE TRUTH"',
    #                   'S08E03 - "SILENCE"', 'S08E04 - "THE QUEEN\'S MAN"',
    #                   'S08E05 - "LAST HEARTH"', 'S08E06 - "THE LONELY HILLS"',
    #                   'S08E07 - "WINTERFELL"', 'S08E08 - "SEVEN KINGDOMS"',
    #                   'S08E09 - "THREE QUEENS"',
    #                   'S08E10 - "THE ONE WHO WAS PROMISED"']
    # sub_chapter_num = [4, 4, 3, 3, 9, 7, 5, 7, 6, 4]
    build_toc(chapter_titles, sub_chapter_files, sub_chapter_num)
    create_metadata(chapter_titles, sub_chapter_files, sub_chapter_num)
    create_mimetype_file()
    create_meta_inf()
    create_css_file()
    create_start_file()
    create_epub('GOT-S8.epub')


if __name__ == "__main__":
    runme()
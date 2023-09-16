import os
import fitz
import re

def group_text_to_blocks(words):

  # Create a dictionary to group tuples by their fifth element which is block number 
  grouped_dict = {}

  for tup in words:
      key = tup[5]  # Use the second element as the key
      if key in grouped_dict:
          grouped_dict[key].append(tup)
      else:
          # print(key)
          grouped_dict[key] = [tup]

  # Convert the dictionary values to a list of lists
  list_of_lists = list(grouped_dict.values())

  return list_of_lists

def get_blocks(doc):
  blocks = []
  texts = []
  i = 0
  for i, page in enumerate(doc):
      block = page.get_text("blocks")
      text = page.get_text("words")

      # page_bbox =
      text = group_text_to_blocks(text)
      # print(len(block), len(text))
      # print((text))
      # print((block))

      new_block = []
      j = 0

      for x0, y0, x1, y1, t, b, _ in block:
        tt = t.replace('\n', " ")
        if t[:7] != "<image:" and not tt.isspace():
          new_block.append((x0, y0, x1, y1, t, b, i, text[j]))
          j+=1

      #new_block format (0 - x0,1 - y0,2 - x1,3 - y1,4 - block_text,5 - block_no within a page,6 - page no,7 - tuple of individual words)

      blocks.extend(new_block)
  return blocks

def drop_non_paras(doc, blocks):
  import math
  new_blocks = []
  for block in blocks: #for each block

    if not re.search("[.]{5,}", block[4]):
      # print(block[4])
      page = doc.load_page(block[6])

      pix = page.get_pixmap()
      pix_width = pix.width

      width = abs(block[0] - block[2])
      if width > pix_width*(1/2) and not block[4].isupper() and len(block[7]) > 15 : # check if width of a para is less than 1/2 of the page width or if the block contains text which is all upper
        avg_space = []
        ideal_space = 20
        # print(block[7])
        for i in range(len(block[7]) - 1): # for each word in each block
          if math.floor(block[7][i][3]) == math.floor(block[7][i + 1][3]): #check if the consecutive words are in the same line.
            avg_space.append(abs(block[7][i][2] - block[7][i + 1][0]), )
            # print(abs(block[7][i][2] - block[7][i + 1][0]), block[7][i][4], block[7][i+1][4]) #get distance/ space btw consecutive words
            # print("ehh")
        if len(avg_space) != 0:
          block_avg_space = sum(avg_space)/ len(avg_space)
          # print("avg", block_avg_space)


          if block_avg_space <= 5:
            new_blocks.append(block)
            # print("here", avg_space,  block_avg_space, block[4])

  return new_blocks
    
def get_json(blocks):
# converting the list of lists into suitable json
  final_list = []
  for block in blocks:
    block_json = {"page_no" : block[6],
                  "bbox" : ( block[0], block[1], block[2], block[3]),
                  "text" : block[4]
                  }
    final_list.append(block_json)
  
  return final_list
    
def extract_pragraphs(doc_path):
  doc_path = doc_path
  doc = fitz.open(doc_path)

  blocks = get_blocks(doc)
  blocks = drop_non_paras(doc, blocks)

  final_blocks = get_json(blocks)

  return final_blocks


pdf_path = 'Wolters-Kluwer-2022-Annual Report-1.pdf'
list_pragraphs=extract_pragraphs(pdf_path)
print(list_pragraphs)

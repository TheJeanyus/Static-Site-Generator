from textnode import TextNode, TextType

def main():
    test_node = TextNode("Hello world!", TextType.PLAIN, None)
    print(test_node)


if __name__ == "__main__":
    main()
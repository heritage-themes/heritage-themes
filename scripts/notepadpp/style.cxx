// Styles a text with one of Notepad++'s Lexilla lexers, for scripts/notepadpp/tokens.py.
//
// Reads from standard input, one item per line: the lexer name; the number of properties, then each as key=value; the
// number of keyword lists, then each as its index, a space and its words; the length of the text in bytes, then the
// text. Writes the style of each byte of the text, separated by spaces.
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

#include "ILexer.h"
#include "Lexilla.h"
#include "TestDocument.h"

namespace {

std::string Line() {
	std::string line;
	std::getline(std::cin, line);
	return line;
}

}

int main() {
	std::ios::sync_with_stdio(false);
	const std::string name = Line();
	Scintilla::ILexer5 *lexer = CreateLexer(name.c_str());
	if (!lexer) {
		std::cerr << "style: no lexer named " << name << "\n";
		return 1;
	}
	for (int count = std::stoi(Line()); count > 0; --count) {
		const std::string property = Line();
		const size_t equals = property.find('=');
		lexer->PropertySet(property.substr(0, equals).c_str(), property.substr(equals + 1).c_str());
	}
	for (int count = std::stoi(Line()); count > 0; --count) {
		const std::string list = Line();
		const size_t space = list.find(' ');
		lexer->WordListSet(std::stoi(list.substr(0, space)), space == std::string::npos ? "" : list.c_str() + space + 1);
	}
	const size_t length = std::stoul(Line());
	std::string text(length, '\0');
	std::cin.read(text.data(), static_cast<std::streamsize>(length));
	if (static_cast<size_t>(std::cin.gcount()) != length) {
		std::cerr << "style: the text is shorter than " << length << " bytes\n";
		return 1;
	}

	TestDocument document;
	document.Set(text);
	lexer->Lex(0, document.Length(), 0, &document);
	lexer->Fold(0, document.Length(), 0, &document);
	for (Sci_Position i = 0; i < document.Length(); ++i) {
		std::cout << (i ? " " : "") << static_cast<int>(static_cast<unsigned char>(document.StyleAt(i)));
	}
	std::cout << "\n";
	lexer->Release();
	return 0;
}

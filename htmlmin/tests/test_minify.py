# -*- coding: utf-8 -*-
import unittest

from htmlmin.minify import html_minify
from nose.tools import assert_equals
from os.path import abspath, dirname, join

resources_path = lambda *paths: abspath(join(dirname(__file__), 'resources', *paths))

class TestMinify(unittest.TestCase):

    def _get_normal_and_minified_content_from_html_files(self, filename):
        html_file = resources_path('%s.html' % filename)
        html_file_minified = resources_path('%s_minified.html' % filename)

        html = open(html_file).read()
        html_minified = open(html_file_minified).read().strip('\n')

        return html, html_minified

    def test_complete_html_should_be_minified(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_menu')
        assert_equals(html_minified, html_minify(html))

    def test_html_with_blank_lines_should_be_minify(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_blank_lines')
        assert_equals(html_minified, html_minify(html))

    def test_should_not_minify_content_from_script_tag(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_javascript')
        assert_equals(html_minified, html_minify(html))

    def test_html_should_be_minified(self):
        html = "<html>   <body>some text here</body>    </html>"
        html_minified = "<!DOCTYPE html><html><body>some text here</body></html>"
        assert_equals(html_minified, html_minify(html))

    def test_minify_function_should_return_a_str_object(self):
        html = "<html>   <body>some text here</body>    </html>"
        html_minified = html_minify(html)
        assert_equals(str, type(html_minified))

    def test_minify_should_respect_encoding(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('blogpost')
        assert_equals(html_minified, html_minify(html))

    def test_minify_should_always_include_doctype(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('without_doctype')
        assert_equals(html_minified, html_minify(html))

    def test_should_exclude_comments_by_default(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_comments_to_exclude')
        assert_equals(html_minified, html_minify(html))

    def test_should_be_able_to_not_exclude_comments(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_comments')
        assert_equals(html_minified, html_minify(html, ignore_comments=False))

    def test_should_be_able_to_exclude_multiline_comments(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_multiple_line_comments')
        assert_equals(html_minified, html_minify(html))

    def test_should_be_able_to_exclude_multiple_comments_on_a_page(self):
        html, html_minified = self._get_normal_and_minified_content_from_html_files('with_multiple_comments')
        assert_equals(html_minified, html_minify(html))
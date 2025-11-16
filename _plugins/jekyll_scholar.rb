# Unescape HTML in the prefix and suffix of elements in the CLS.
# Required to be able to insert HTML tags within the CLS.
# Thanks to
# https://github.com/m-pilia/m-pilia.github.io/blob/source/_plugins/unescape_cls_html.rb
# via https://martinopilia.com/posts/2020/02/22/migration.html#fn:1.
require 'cgi'
require 'citeproc/ruby'

class CiteProc::Ruby::Formats::Html
  def prefix
    CGI.unescape_html options[:prefix]
  end

  def suffix
    CGI.unescape_html options[:suffix]
  end
end

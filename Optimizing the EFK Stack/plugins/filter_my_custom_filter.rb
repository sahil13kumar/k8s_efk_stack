require 'fluent/plugin/filter'

class Fluent::Plugin::MyCustomFilter < Fluent::Plugin::Filter
  Fluent::Plugin.register_filter('my_custom_filter', self)

  config_param :additional_data, :string, default: 'static_info'

  def filter(tag, time, record)
    record['additional_data'] = @additional_data
    record
  end
end
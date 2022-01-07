<template>
    <plotly />
</template>

<figure>
{
    {% set line_colors = var('line_colors') %}
    {% set fill_colors = var('fill_colors') %}
    {% set font_family = var('font_family') %}
    {% set font_color = var('font_color') %}
    {% set font_size = var('font_size') %}
    {% set tickfont_family = var('tickfont_family') %}
    {% set tickfont_color = var('tickfont_color') %}
    {% set tickfont_size = var('tickfont_size') %}
    {% set hover_label_bg = var('hover_label_bg') %}

    "data": [
        {% for measure in measures %}
        {
            "type": "scatter",
            "mode": "lines",
            "line": {
                {% if line_colors %}
                "color": "{{ line_colors[loop.index-1] }}",
                {% else %}
                "color" : "rgba(29, 34, 96,1)",
                {% endif %}

                {% if config.line_type %}
                "shape": "{{ config.line_type }}"
                {% else %}
                "shape": "spline"
                {% endif %},
                
                "smoothing": 0.45,
                "width": 1.45
            },
            "connectgaps": true,

            {% if not config.stacked %}

            {% if config.fill_type=='no fill' %}
            "fill" : "none"
            {% elif config.fill_type=='x fill' %}
            "fill" : "tozerox"
            {% elif config.fill_type=='y fill' %}
            "fill" : "tozeroy"
            {% elif config.fill_type=='previous y' %}
            "fill" : "tonexty"
            {% elif config.fill_type=='previous x' %}
            "fill" : "tonextx"
            {% else %}
            "fill" : "tozeroy"
            {% endif %},

            {% else %}
            "stackgroup": "one",
            {% endif %}

            {% if fill_colors %}
            "fillcolor": "{{ fill_colors[loop.index-1] }}",
            {% else %}
            "fillcolor": "rgb(236, 238, 245)",
            {% endif %}

            {% if column_tag(measure, 'yaxis_right') %}
            "yaxis": "y2",
            {% else %}
            "yaxis": "y1",
            {% endif %}

            "xaxis": "x2",
            "marker" : {
                {% if line_colors %}
                "color" : "{{ line_colors[loop.index-1] }}",
                {% else %}
                "color" : "rgba(29, 34, 96,1)",
                {% endif %}
                "size": 3
            },
            "name": "{{ column_metadata(measure,'label') }}",
            "x": {{ column_data(dimensions[0]) }},
            "y": {{ column_data(measure) }}
        }{% if not loop.last %},{%endif%}
        {% endfor %}   
    ],
    "layout" : {
        "hovermode": "x unified",
        "plot_bgcolor" : "rgba(0,0,0,0)",
        "paper_bgcolor" : "rgba(0,0,0,0)",
        "font" : {
            
            {% if font_family %}
             "family" : "{{ font_family }}"
            {% else %}
            "family": "Open Sans"
            {% endif %},

            {% if font_color %}
             "color" : "{{ font_color }}"
            {% else %}
            "color" : "#161F3D"
            {% endif %},
            
            {% if font_size %}
             "size" : "{{ font_size }}"
            {% else %}
            "size": 10
            {% endif %}
        },
        "xaxis" : {
            {% if config.x_grid=='hide' %}
            "showgrid": false
            {% elif config.x_grid=='show' %}
            "showgrid": true
            {% else %}
            "showgrid": false
            {% endif %},

            {% if config.x_labels=='hide' %}
            "showticklabels": false
            {% elif config.x_labels=='show' %}
            "showticklabels": true
            {% else %}
            "showticklabels": true
            {% endif %},

            {% if config.x_axis=='hide' %}
            "zeroline" : false
            {% elif config.x_axis=='show' %}
            "zeroline" : true
            {% else %}
            "zeroline" : true
            {% endif %},

            "linewidth" : 7,
            "linecolor" : "rgba(0,0,0,0)",
            "tickfont" : {
                {% if tickfont_family %}
                "family" : "{{ tickfont_family }}"
                {% else %}
                "family": "Open Sans"
                {% endif %},

                {% if tickfont_color %}
                "color" : "{{ tickfont_color }}"
                {% else %}
                "color" : "#161F3D"
                {% endif %},
            
                {% if tickfont_size %}
                "size" : "{{ tickfont_size }}"
                {% else %}
                "size": 11
                {% endif %}
              
            },
            "color" : "rgba(0, 0, 0, 0.65)",
            "showline" : false,
            "title" : {
                {% if config.x_title %}
                "text": "{{ config.x_title }}"
                {% else %}
                "text" : ""
                {% endif %},
                "font": {
                    {% if font_family %}
                    "family" : "{{ font_family }}"
                    {% else %}
                    "family": "Open Sans"
                    {% endif %},
                    {% if font_color %}
                    "color" : "{{ font_color }}"
                    {% else %}
                    "color" : "#161F3D"
                    {% endif %},
                    {% if font_size %}
                    "size" : "{{ font_size }}"
                    {% else %}
                    "size": 11
                    {% endif %}
                }
            }

        },
        "xaxis2": {
            {% if config.x_grid=='hide' %}
            "showgrid": false
            {% elif config.x_grid=='show' %}
            "showgrid": true
            {% else %}
            "showgrid": false
            {% endif %},

            {% if config.x_labels=='hide' %}
            "showticklabels": false
            {% elif config.x_labels=='show' %}
            "showticklabels": true
            {% else %}
            "showticklabels": true
            {% endif %},

            {% if config.x_axis=='hide' %}
            "zeroline" : false
            {% elif config.x_axis=='show' %}
            "zeroline" : true
            {% else %}
            "zeroline" : true
            {% endif %},

            
            "linewidth" : 7,
            "linecolor" : "rgba(0,0,0,0)",
            "tickfont" : {
                {% if tickfont_family %}
                "family" : "{{ tickfont_family }}"
                {% else %}
                "family": "Open Sans"
                {% endif %},

                {% if tickfont_color %}
                "color" : "{{ tickfont_color }}"
                {% else %}
                "color" : "#161F3D"
                {% endif %},
            
                {% if tickfont_size %}
                "size" : "{{ tickfont_size }}"
                {% else %}
                "size": 11
                {% endif %}
            },
            "title" : {
                {% if config.x_title %}
                "text": "{{ config.x_title }}"
                {% else %}
                "text" : ""
                {% endif %},
                "font": {
                    {% if font_family %}
                    "family" : "{{ font_family }}"
                    {% else %}
                    "family": "Open Sans"
                    {% endif %},
                    {% if font_color %}
                    "color" : "{{ font_color }}"
                    {% else %}
                    "color" : "#161F3D"
                    {% endif %},
                    {% if font_size %}
                    "size" : "{{ font_size }}"
                    {% else %}
                    "size": 11
                    {% endif %}
                }
            }
        },
        "yaxis" : {
            "overlaying": "y2",

            {% if config.y_grid=='hide' %}
            "showgrid": false
            {% elif config.y_grid=='show' %}
            "showgrid": true
            {% else %}
            "showgrid": false
            {% endif %},

            {% if config.y_labels=='hide' %}
            "showticklabels": false
            {% elif config.y_labels=='show' %}
            "showticklabels": true
            {% else %}
            "showticklabels": true
            {% endif %},

            {% if config.y_axis=='hide' %}
            "zeroline" : false
            {% elif config.y_axis=='show' %}
            "zeroline" : true
            {% else %}
            "zeroline" : true
            {% endif %},

            
            "linewidth" : 7,
            "linecolor" : "rgba(0,0,0,0)",
            "tickfont" : {
                {% if tickfont_family %}
                "family" : "{{ tickfont_family }}"
                {% else %}
                "family": "Open Sans"
                {% endif %},

                {% if tickfont_color %}
                "color" : "{{ tickfont_color }}"
                {% else %}
                "color" : "#161F3D"
                {% endif %},
            
                {% if tickfont_size %}
                "size" : "{{ tickfont_size }}"
                {% else %}
                "size": 11
                {% endif %}
            },
            "color" : "rgba(0, 0, 0, 0.65)",
            "zerolinecolor" : "#eee",
            "gridcolor" : "#eee",
            "title" : {
                {% if config.y_title %}
                "text": "{{ config.y_title }}"
                {% else %}
                "text" : ""
                {% endif %},
                "font": {
                    {% if font_family %}
                    "family" : "{{ font_family }}"
                    {% else %}
                    "family": "Open Sans"
                    {% endif %},
                    {% if font_color %}
                    "color" : "{{ font_color }}"
                    {% else %}
                    "color" : "#161F3D"
                    {% endif %},
                    {% if font_size %}
                    "size" : "{{ font_size }}"
                    {% else %}
                    "size": 11
                    {% endif %}
                }
            },
            "side": "left"
        },
        "yaxis2" : {
            "showgrid": false,

            {% if config.y_grid=='hide' %}
            "showgrid": false
            {% elif config.y_grid=='show' %}
            "showgrid": true
            {% else %}
            "showgrid": false
            {% endif %},

            {% if config.y_labels=='hide' %}
            "showticklabels": false
            {% elif config.y_labels=='show' %}
            "showticklabels": true
            {% else %}
            "showticklabels": true
            {% endif %},

            {% if config.y_axis=='hide' %}
            "zeroline" : false
            {% elif config.y_axis=='show' %}
            "zeroline" : true
            {% else %}
            "zeroline" : true
            {% endif %},

            "side": "right",
            "linewidth" : 7,
            "linecolor" : "rgba(0,0,0,0)",
            "tickfont" : {
                {% if tickfont_family %}
                "family" : "{{ tickfont_family }}"
                {% else %}
                "family": "Open Sans"
                {% endif %},

                {% if tickfont_color %}
                "color" : "{{ tickfont_color }}"
                {% else %}
                "color" : "#161F3D"
                {% endif %},
            
                {% if tickfont_size %}
                "size" : "{{ tickfont_size }}"
                {% else %}
                "size": 11
                {% endif %}
            },
            "color" : "rgba(0, 0, 0, 0.65)",
            "zerolinecolor" : "#eee",
            "gridcolor" : "#eee",
            "title" : {
                {% if config.y_title %}
                "text": "{{ config.y_title }}"
                {% else %}
                "text" : ""
                {% endif %},
                "font": {
                    {% if font_family %}
                    "family" : "{{ font_family }}"
                    {% else %}
                    "family": "Open Sans"
                    {% endif %},
                    {% if font_color %}
                    "color" : "{{ font_color }}"
                    {% else %}
                    "color" : "#161F3D"
                    {% endif %},
                    {% if font_size %}
                    "size" : "{{ font_size }}"
                    {% else %}
                    "size": 11
                    {% endif %}
                }
            }
        },
        "hoverlabel": {
            {% if hover_label_bg %}
            "bgcolor" : "{{ hover_label_bg }}"
            {% else %}
            "bgcolor" : "rgba(232,230,230,0.7)"
            {% endif %},

            {% if hover_label_bg %}
            "bordercolor" : "{{ hover_label_bg }}"
            {% else %}
            "bordercolor" : "rgba(232,230,230,0.7)"
            {% endif %} 
        },
        "autosize": true,
        "automargin": true,

        {% if config.legend=='show' %}
        "showlegend": true
        {% elif config.legend=='hide' %}
        "showlegend": false
        {% else %}
        "showlegend":false
        {% endif %},
         
        "legend" : {
            "x": 0.01,
            "y": 1.1
        },
        {% if config.margin =='small' %}
        "margin" : {
          "l" : 10,
          "r" : 10,
          "t":10,
          "b":10,
          "pad": 0
       }
       {% else %}
       "margin" : {
          "l" : 70,
          "r" : 30,
          "t":30,
          "b":60,
          "pad": 0
       }
       {% endif %}
    }
}
</figure>

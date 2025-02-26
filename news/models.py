from datetime import date, datetime

from django.db import models
from django.http import HttpRequest
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail import blocks as wagtail_blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.search import index

from blocks.blocks import (
    FormattedImageChooserStructBlock,
    HeadingBlock,
    PullQuoteBlock,
    SpacerBlock,
)
from common.models import DrupalFields
from documents.blocks import DocumentEmbedBlock


class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = [
        "home.HomePage",
    ]
    subpage_types: list[str] = [
        "NewsTopicIndexPage",
        "NewsTypeIndexPage",
        "NewsItem",
    ]
    max_count = 1

    def get_context(
        self,
        request: HttpRequest,
        *args: tuple,
        **kwargs: dict,
    ) -> dict[str, list]:
        context = super().get_context(request)

        current_year = datetime.now().year
        earliest = NewsItem.objects.order_by("publication_date").first()

        if earliest is None:
            earliest_year = current_year
        else:
            earliest_year = earliest.publication_date.year

        # Get inclusive set of years from earliest to current (hence +1)
        context["news_years"] = range(earliest_year, current_year + 1)

        default_year = current_year
        context["selected_year"] = int(request.GET.get("year", default_year))

        # Filter live (not draft) news items
        # and items from selected year
        # reverse chronological order
        context["news_items"] = (
            NewsItem.objects.live()
            .filter(publication_date__year=context["selected_year"])
            .order_by("-publication_date")
        )

        return context


class NewsTopicIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = [
        "NewsIndexPage",
    ]
    subpage_types: list[str] = [
        "NewsTopic",
    ]
    max_count = 1


class NewsTopic(Page):
    intro = RichTextField(blank=True)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("intro"),
    ]

    # Hide the settings panels
    settings_panels: list[str] = []

    parent_page_types = [
        "NewsTopicIndexPage",
    ]
    subpage_types: list[str] = []


class NewsTypeIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    parent_page_types = [
        "NewsIndexPage",
    ]
    subpage_types: list[str] = [
        "NewsType",
    ]
    max_count = 1


class NewsType(Page):
    intro = RichTextField(blank=True)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("intro"),
    ]

    # Hide the settings panels
    settings_panels: list[str] = []

    parent_page_types = [
        "NewsTypeIndexPage",
    ]
    subpage_types: list[str] = []


class NewsItemTag(TaggedItemBase):
    content_object = ParentalKey(
        "news.NewsItem",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class NewsItem(DrupalFields, Page):
    teaser = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Briefly summarize the news item for display in news lists",
    )
    publication_date = models.DateField(default=date.today)
    body = StreamField(
        [
            ("heading", HeadingBlock()),
            (
                "rich_text",
                wagtail_blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "ol",
                        "ul",
                        "hr",
                        "link",
                        "document-link",
                        "superscript",
                        "superscript",
                        "strikethrough",
                        "blockquote",
                    ],
                ),
            ),
            ("pullquote", PullQuoteBlock()),
            ("image", FormattedImageChooserStructBlock(classname="full title")),
            ("document", DocumentEmbedBlock()),
            ("spacer", SpacerBlock()),
            ("embed", EmbedBlock()),
        ],
        use_json_field=True,
    )
    tags = ClusterTaggableManager(
        through=NewsItemTag,
        blank=True,
    )
    body_migrated = models.TextField(
        help_text="Used only for content from old Drupal website.",
        null=True,
        blank=True,
    )
    drupal_node_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    news_topic = models.ForeignKey(
        NewsTopic,
        on_delete=models.PROTECT,
        related_name="news_items",
        null=True,
        blank=True,
    )
    news_type = models.ForeignKey(
        NewsType,
        on_delete=models.PROTECT,
        related_name="news_items",
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("teaser"),
        FieldPanel("body"),
        MultiFieldPanel(
            heading="Metadata",
            children=[
                FieldPanel("publication_date"),
                FieldPanel("news_topic"),
                FieldPanel("news_type"),
                FieldPanel("tags"),
            ],
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("teaser"),
        index.SearchField("body"),
        index.RelatedFields(
            "news_topic",
            [
                index.SearchField("title"),
            ],
        ),
        index.RelatedFields(
            "tags",
            [
                index.SearchField("name"),
            ],
        ),
    ]

    parent_page_types = [
        "NewsIndexPage",
    ]
    subpage_types: list[str] = []

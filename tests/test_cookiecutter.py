"""
    Tests cookiecutter baking process and rendered content
"""


def test_project_tree(cookies):
    result = cookies.bake(extra_context={
        'project_name': '--pytest-cookies--',
        'source_code_repo': '1'
    })
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == '--pytest-cookies--'
    assert result.project.isdir()
    assert result.project.join('buildspec.yaml').isfile()
    assert result.project.join('pipeline.yaml').isfile()
    assert result.project.join('Pipeline-Instructions.md').isfile()
    assert result.project.join('pipeline-sample.png').isfile()


def test_codecommit_content(cookies):
    result = cookies.bake(extra_context={
        'project_name': '--pytest-cookies--',
        'source_code_repo': "CodeCommit"
    })
    pipeline = result.project.join('pipeline.yaml')
    app_content = pipeline.readlines()
    app_content = ''.join(app_content)

    contents = ("AWS CodeCommit", "BranchName", "RepositoryName",
                "arn:aws:codecommit", "CodeCommitRepositoryHttpUrl",
                "CodeCommitRepositorySshUrl")

    for content in contents:
        assert content in app_content


def test_pipeline_content(cookies):
    result = cookies.bake(extra_context={
        'project_name': '--pytest-cookies--',
        'source_code_repo': "CodeCommit"
    })
    pipeline = result.project.join('pipeline.yaml')
    app_content = pipeline.readlines()
    # pprint(app_content)
    app_content = ''.join(app_content)

    contents = ("Amazon S3", "AWS CodeBuild", "AWS CloudFormation",
                "BuildArtifactsBucket", "BUILD_OUTPUT_BUCKET",
                "CodePipelineExecutionRole", "Name: SourceCodeRepo",
                "Category: Build", "Category: Deploy", "BuildArtifactAsZip",
                "SourceCodeAsZip")

    for content in contents:
        assert content in app_content


# FIXME: Couldn't figure out why options aren't accepted in pytest-cookies
# def test_github_content(cookies):
